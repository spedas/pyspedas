import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from pyspedas.utilities.zenodo_draft import ZenodoDraftClient, ZenodoError


def deposition(record_id, concept="123", *, submitted=False, title="Project"):
    return {
        "id": record_id,
        "conceptrecid": concept,
        "submitted": submitted,
        "metadata": {
            "title": title,
            "creators": [{"name": "Example, Ada"}] if title == "Project" else [],
            "prereserve_doi": {"doi": f"10.5281/zenodo.{record_id}"},
        },
        "files": [],
        "links": {
            "self": f"https://zenodo.example/depositions/{record_id}",
            "bucket": "https://zenodo.example/bucket",
            "newversion": "https://zenodo.example/newversion",
        },
    }


class ZenodoDraftClientTests(unittest.TestCase):
    def setUp(self):
        self.client = ZenodoDraftClient("token")

    def test_published_record_is_not_a_draft(self):
        self.assertFalse(self.client._is_draft(deposition(100, submitted=True), "123"))

    def test_reserve_reuses_unpublished_draft(self):
        draft = deposition(200)
        self.client.find_draft = MagicMock(return_value=draft)
        result = self.client.reserve("123")
        self.assertEqual(result["action"], "reused")
        self.assertEqual(result["doi"], "10.5281/zenodo.200")

    def test_reserve_creates_version_without_rewriting_metadata(self):
        published = deposition(100, submitted=True)
        draft = deposition(200)
        self.client.find_draft = MagicMock(return_value=None)
        self.client.latest_published = MagicMock(return_value=published)
        self.client._json = MagicMock(return_value={"links": {"latest_draft": "https://zenodo.example/200"}})
        self.client.deposition = MagicMock(return_value=draft)
        result = self.client.reserve("123")
        self.assertEqual(result["action"], "created")
        self.client._json.assert_called_once_with("POST", published["links"]["newversion"])

    def test_reserve_repairs_old_zenodraft_metadata(self):
        empty = deposition(200, title="Untitled in 123")
        repaired = deposition(200)
        published = deposition(100, submitted=True)
        self.client.find_draft = MagicMock(return_value=empty)
        self.client.latest_published = MagicMock(return_value=published)
        self.client.update_metadata_from = MagicMock(return_value=repaired)
        result = self.client.reserve("123")
        self.assertEqual(result["action"], "repaired")
        self.client.update_metadata_from.assert_called_once_with(empty, published)

    def test_metadata_repair_omits_server_managed_doi_and_historical_grants(self):
        draft = deposition(200)
        published = deposition(100, submitted=True)
        published["metadata"]["doi"] = "10.5281/zenodo.100"
        published["metadata"]["grants"] = [{"id": "027ka1x80::NAS5-02099"}]
        self.client._json = MagicMock(return_value=draft)
        self.client.update_metadata_from(draft, published)
        payload = self.client._json.call_args.kwargs["json"]["metadata"]
        self.assertNotIn("doi", payload)
        self.assertNotIn("prereserve_doi", payload)
        self.assertNotIn("grants", payload)
        self.assertEqual(payload["creators"], published["metadata"]["creators"])

    def test_replace_files_checks_doi_before_writes(self):
        self.client.find_draft = MagicMock(return_value=deposition(200))
        self.client._json = MagicMock()
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "release.zip"
            filename.touch()
            with self.assertRaises(ZenodoError):
                self.client.replace_files("123", "10.5281/zenodo.999", filename)
        self.client._json.assert_not_called()


if __name__ == "__main__":
    unittest.main()
