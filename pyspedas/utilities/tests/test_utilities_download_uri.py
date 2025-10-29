import os
import time
import requests
import unittest
import subprocess

from pyspedas.utilities.download import download

class DownloadTestCases(unittest.TestCase):
    """
    Cloud Awareness Unit Tests

    Depends upon moto[server] package. Install via:
        pip install moto[server]

    These tests essentially create a local mock-AWS server as a background
    process at port 3000.
    Note: The environment variables are used as mock credentials in order
          to avoid having to pass the endpoint url to fsspec calls.
    """

    @classmethod
    def setUpClass(cls):
        # Start the moto server for S3 in the background
        # https://github.com/getmoto/moto/issues/4418
        cls.moto_server = subprocess.Popen(
                ["moto_server", "-p3000"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Allow the server to start properly
        time.sleep(2)

        # Set up mock AWS environment variables (fake credentials)
        os.environ["AWS_ACCESS_KEY_ID"] = "test"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

        # Set environment to use the local Moto S3 server
        # S3 ENDPOINT for fsspec
        # ENDPOINT URL for cdflib's boto3
        os.environ["AWS_S3_ENDPOINT"] = "http://localhost:3000"
        os.environ["AWS_ENDPOINT_URL"] = "http://localhost:3000"

        # Create a bucket using direct HTTP requests
        bucket_name = "test-bucket"
        response = requests.put(f"http://localhost:3000/{bucket_name}")
        assert response.status_code == 200, "Bucket creation failed"

    @classmethod
    def tearDownClass(cls):
        # Terminate the moto server after tests
        cls.moto_server.terminate()
        cls.moto_server.communicate()

    #==========================================================================
    # Adapted unit tests (from download_tests.py) for AWS-specific URI testing.
    def test_local_path(self):
        # Remote/AWS details
        bucket_name = "test-bucket"
        s3_url = f"s3://{bucket_name}"

        # Include mock AWS credentials and endpoints
        os.environ["AWS_ACCESS_KEY_ID"] = "test"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        os.environ["AWS_S3_ENDPOINT"] = "http://localhost:3000"
        os.environ["AWS_ENDPOINT_URL"] = "http://localhost:3000"

        # specifying local_path changes the local data directory
        files = download(
                local_path=s3_url + "/psp_data/spc/13",
                remote_file="https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf"
        )

        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == s3_url + "/psp_data/spc/13/psp_swp_spc_l3i_20190401_v01.cdf")

    def test_remote_path(self):
        # Remote/AWS details
        bucket_name = "test-bucket"
        s3_url = f"s3://{bucket_name}"

        # Include mock AWS credentials and endpoints
        os.environ["AWS_ACCESS_KEY_ID"] = "test"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        os.environ["AWS_S3_ENDPOINT"] = "http://localhost:3000"
        os.environ["AWS_ENDPOINT_URL"] = "http://localhost:3000"

        # download (if not already downloaded from prior tests)
        files = download(
                local_path=s3_url + "/psp/sweap/spc/l3/l3i/2019",
                remote_file="https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf"
        )
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == s3_url + "/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf")

        # stream from remote
        with self.assertLogs(level='INFO') as log:
            files = download(
                    remote_path=s3_url,
                    remote_file="/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf"
            )
            self.assertIn("Streaming from remote", log.output[0])

    def test_force_download(self):
        # Remote/AWS details
        bucket_name = "test-bucket"
        s3_url = f"s3://{bucket_name}"

        # Include mock AWS credentials and endpoints
        os.environ["AWS_ACCESS_KEY_ID"] = "test"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        os.environ["AWS_S3_ENDPOINT"] = "http://localhost:3000"
        os.environ["AWS_ENDPOINT_URL"] = "http://localhost:3000"

        files = download(
                local_path=s3_url + "/themis/tha/l1/state/2007",
                remote_file="https://spdf.gsfc.nasa.gov/pub/data/themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf"
        )
        self.assertTrue(len(files) == 1)
        print(files)
        self.assertTrue(files[0] == s3_url + "/themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf")

        # Download the same file without force_download, should not re-download
        with self.assertLogs(level='INFO') as log:
            files = download(
                    local_path=s3_url + "/themis/tha/l1/state/2007",
                    remote_file="https://spdf.gsfc.nasa.gov/pub/data/themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf"
            )
            self.assertIn("File is current", log.output[0])

        # Download the same file with force_download, should re-download
        with self.assertLogs(level='INFO') as log:
            files = download(
                    local_path=s3_url + "/psp_data/spc/13",
                    remote_file="https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf",
                    force_download=True
            )
            self.assertIn("Downloading", log.output[0])

if __name__ == '__main__':
    unittest.main(verbosity=2)
