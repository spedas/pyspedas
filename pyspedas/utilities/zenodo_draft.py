"""Small, conservative client for managing versioned Zenodo draft deposits.

The client intentionally has no publish operation.  Read requests are retried;
write requests are not, because a timed-out write may have succeeded remotely.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ZenodoError(RuntimeError):
    """A Zenodo response was unsuccessful, malformed, or unsafe to act on."""


class ZenodoDraftClient:
    def __init__(self, token: str, *, sandbox: bool = False, timeout=(15, 90)):
        if not token or any(character.isspace() for character in token):
            raise ValueError("Zenodo token is missing or contains whitespace")
        self.base_url = "https://sandbox.zenodo.org" if sandbox else "https://zenodo.org"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        retry = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(("GET", "HEAD", "OPTIONS")),
            respect_retry_after_header=True,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def _json(self, method: str, url: str, **kwargs) -> Any:
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        except requests.RequestException as error:
            qualifier = "; the write may have succeeded—rerun the command to reconcile state" if method not in ("GET", "HEAD", "OPTIONS") else ""
            raise ZenodoError(f"Zenodo {method} request failed{qualifier}: {error}") from error
        if not response.ok:
            body = response.text[:2000]
            raise ZenodoError(f"Zenodo {method} {url} returned HTTP {response.status_code}: {body}")
        if not response.content:
            return None
        try:
            return response.json()
        except requests.JSONDecodeError as error:
            raise ZenodoError(
                f"Zenodo {method} {url} returned non-JSON content: {response.text[:300]}"
            ) from error

    def deposition(self, deposition_id: str | int) -> dict[str, Any]:
        return self._json("GET", f"{self.base_url}/api/deposit/depositions/{deposition_id}")

    @staticmethod
    def _is_draft(details: dict[str, Any], concept_id: str) -> bool:
        return details.get("submitted") is False and str(details.get("conceptrecid")) == concept_id

    def find_draft(self, concept_id: str) -> dict[str, Any] | None:
        depositions = self._json("GET", f"{self.base_url}/api/deposit/depositions")
        if not isinstance(depositions, list):
            raise ZenodoError("Zenodo depositions response was not a list")
        seen: set[str] = set()
        for item in depositions:
            if str(item.get("conceptrecid")) != concept_id:
                continue
            candidates = [item.get("id"), item.get("links", {}).get("latest_draft")]
            for candidate in candidates:
                if not candidate:
                    continue
                deposition_id = str(candidate).rstrip("/").rsplit("/", 1)[-1]
                if deposition_id in seen:
                    continue
                seen.add(deposition_id)
                details = self.deposition(deposition_id)
                if self._is_draft(details, concept_id):
                    return details
        return None

    def latest_published(self, concept_id: str) -> dict[str, Any]:
        records = self._json(
            "GET",
            f"{self.base_url}/api/records",
            params={"q": f"conceptrecid:{concept_id}", "sort": "mostrecent", "size": 1},
        )
        try:
            record_id = records["hits"]["hits"][0]["id"]
        except (KeyError, IndexError, TypeError) as error:
            raise ZenodoError(f"No published record found for concept {concept_id}") from error
        details = self.deposition(record_id)
        if details.get("submitted") is not True:
            raise ZenodoError(f"Record {record_id} is not a published deposition")
        return details

    def update_metadata_from(self, draft: dict[str, Any], published: dict[str, Any]) -> dict[str, Any]:
        metadata = dict(published.get("metadata", {}))
        metadata.pop("doi", None)
        metadata.pop("prereserve_doi", None)
        return self._json("PUT", draft["links"]["self"], json={"metadata": metadata})

    def reserve(self, concept_id: str) -> dict[str, str]:
        if not concept_id.isdigit():
            raise ValueError("concept_id must contain only digits")
        draft = self.find_draft(concept_id)
        action = "reused"
        if draft is None:
            published = self.latest_published(concept_id)
            new_version_url = published.get("links", {}).get("newversion")
            if not new_version_url:
                raise ZenodoError("Latest published deposition has no new-version link")
            created = self._json("POST", new_version_url)
            draft_url = created.get("links", {}).get("latest_draft") or created.get("links", {}).get("self")
            if not draft_url:
                raise ZenodoError("New-version response did not identify the draft")
            draft = self.deposition(str(draft_url).rstrip("/").rsplit("/", 1)[-1])
            action = "created"
        elif str(draft.get("metadata", {}).get("title", "")).startswith("Untitled in ") and not draft.get("metadata", {}).get("creators"):
            draft = self.update_metadata_from(draft, self.latest_published(concept_id))
            action = "repaired"

        if not self._is_draft(draft, concept_id):
            raise ZenodoError("Selected deposition is not an unpublished draft in the requested concept")
        try:
            doi = draft["metadata"]["prereserve_doi"]["doi"]
            draft_id = str(draft["id"])
        except (KeyError, TypeError) as error:
            raise ZenodoError("Draft has no pre-reserved DOI") from error
        return {
            "action": action,
            "id": draft_id,
            "doi": doi,
            "url": f"{self.base_url}/uploads/{draft_id}",
        }

    def replace_files(self, concept_id: str, expected_doi: str, filename: Path) -> dict[str, str]:
        draft = self.find_draft(concept_id)
        if draft is None or not self._is_draft(draft, concept_id):
            raise ZenodoError(f"No unpublished draft exists for concept {concept_id}")
        actual_doi = draft.get("metadata", {}).get("prereserve_doi", {}).get("doi")
        if actual_doi != expected_doi.removeprefix("https://doi.org/"):
            raise ZenodoError(f"Draft DOI {actual_doi} does not match expected DOI {expected_doi}")
        for remote_file in draft.get("files", []):
            self._json("DELETE", remote_file["links"]["self"])
        bucket = draft.get("links", {}).get("bucket")
        if not bucket:
            raise ZenodoError("Draft has no file bucket")
        with filename.open("rb") as stream:
            uploaded = self._json(
                "PUT",
                f"{bucket}/{quote(filename.name)}",
                data=stream,
                headers={"Content-Type": "application/octet-stream"},
            )
        return {
            "id": str(draft["id"]),
            "doi": actual_doi,
            "filename": uploaded.get("key", filename.name),
        }


def _client(sandbox: bool) -> ZenodoDraftClient:
    variable = "ZENODO_SANDBOX_ACCESS_TOKEN" if sandbox else "ZENODO_ACCESS_TOKEN"
    return ZenodoDraftClient(os.environ.get(variable, ""), sandbox=sandbox)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sandbox", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)
    reserve = subparsers.add_parser("reserve")
    reserve.add_argument("--concept", required=True)
    replace = subparsers.add_parser("replace-files")
    replace.add_argument("--concept", required=True)
    replace.add_argument("--expected-doi", required=True)
    replace.add_argument("filename", type=Path)
    args = parser.parse_args()
    client = _client(args.sandbox)
    if args.command == "reserve":
        result = client.reserve(args.concept)
    else:
        result = client.replace_files(args.concept, args.expected_doi, args.filename)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
