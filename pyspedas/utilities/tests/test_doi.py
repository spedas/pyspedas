import unittest
from pathlib import Path

import tomli

from pyspedas.utilities.doi import get_doi


class DoiTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pyproject = Path(__file__).resolve().parents[3] / "pyproject.toml"
        with pyproject.open("rb") as stream:
            cls.urls = tomli.load(stream)["project"]["urls"]

    def test_versioned_doi(self):
        self.assertEqual(get_doi(), self.urls["Versioned_DOI"])

    def test_concept_doi(self):
        self.assertEqual(get_doi("concept"), self.urls["Concept_DOI"])

    def test_invalid_kind(self):
        with self.assertRaises(ValueError):
            get_doi("latest")


if __name__ == "__main__":
    unittest.main()
