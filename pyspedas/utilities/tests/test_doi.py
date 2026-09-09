import unittest
from importlib.metadata import metadata
from pathlib import Path

import tomli

from pyspedas.utilities.doi import get_doi


class DoiTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Tests are run both from a checkout and from an installed wheel.  Wheels
        # do not (and should not) include the repository's pyproject.toml.
        for parent in Path(__file__).resolve().parents:
            pyproject = parent / "pyproject.toml"
            if pyproject.is_file():
                with pyproject.open("rb") as stream:
                    cls.urls = tomli.load(stream)["project"]["urls"]
                break
        else:
            project_urls = metadata("pyspedas").get_all("Project-URL") or []
            cls.urls = dict(
                item.split(", ", 1) for item in project_urls if ", " in item
            )

    def test_versioned_doi(self):
        self.assertEqual(get_doi(), self.urls["Versioned_DOI"])

    def test_concept_doi(self):
        self.assertEqual(get_doi("concept"), self.urls["Concept_DOI"])

    def test_invalid_kind(self):
        with self.assertRaises(ValueError):
            get_doi("latest")


if __name__ == "__main__":
    unittest.main()
