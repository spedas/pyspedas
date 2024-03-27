"""Test functions in the utilities folder."""
import unittest
import logging
from pyspedas import find_ip_address


class UtilTestCases(unittest.TestCase):
    """Test functions in the utilities folder."""

    def test_find_ip_address(self):
        """Show current public IP address """
        ip = find_ip_address()
        print("Current public IP address: %s" % ip)

if __name__ == '__main__':
    unittest.main()
