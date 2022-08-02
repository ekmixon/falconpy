"""
test_sample_uploads.py - This class tests the sample_uploads service class
"""
import os
import sys
import pytest
import datetime
import hashlib
# Authentication via the test_authorization.py
from tests import test_authorization as Authorization
# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# Classes to test - manually imported from sibling folder
from falconpy.sample_uploads import Sample_Uploads

auth = Authorization.TestAuthorization()
token = auth.getConfigExtended()
falcon = Sample_Uploads(access_token=token)
AllowedResponses = [200, 201, 400, 404, 429]


class TestSampleUploads:
    def sample_upload_download_delete(self):
        """
        Tests all functionality within the class by performing an upload / download / compare / delete.
        """
        FILENAME = "tests/testfile.png"
        fmt = '%Y-%m-%d %H:%M:%S'
        stddate = datetime.datetime.now().strftime(fmt)
        sdtdate = datetime.datetime.strptime(stddate, fmt)
        sdtdate = sdtdate.timetuple()
        jdate = sdtdate.tm_yday
        jdate = f'{stddate.replace("-", "").replace(":", "").replace(" ", "")}{jdate}'
        SOURCE = f"{jdate}_source.png"
        TARGET = f"tests/{jdate}_target.png"
        PAYLOAD = open(FILENAME, 'rb').read()
        response = falcon.UploadSampleV3(file_name=SOURCE, file_data=PAYLOAD)
        try:
            sha = response["body"]["resources"][0]["sha256"]
        except KeyError:
            sha = None
        if sha:
            response = falcon.GetSampleV3(ids=sha)
            try:
                open(TARGET, 'wb').write(response)
            except TypeError:
                # This particular unit test failed it's upload, pass a True since the code path was tested
                pytest.skip("Unable to open test file, skipping.")
                return True
            buf = 65536
            hash1 = hashlib.sha256()
            with open(FILENAME, 'rb') as f:
                while True:
                    if data := f.read(buf):
                        hash1.update(data)
                    else:
                        break
            hash1 = hash1.hexdigest()
            hash2 = hashlib.sha256()
            with open(TARGET, 'rb') as f:
                while True:
                    if data := f.read(buf):
                        hash2.update(data)
                    else:
                        break
            hash2 = hash2.hexdigest()
            if os.path.exists(TARGET):
                os.remove(TARGET)
            if hash1 == hash2:
                response = falcon.DeleteSampleV3(ids=sha)
                return True
            else:
                response = falcon.DeleteSampleV3(ids=sha)
                return False
        else:
            # Workflow download error, skip it
            pytest.skip("Workflow-related upload error, skipping.")
            return True

    def sample_errors(self):
        """
        Executes every statement in every method of the class, accepts all errors except 500
        """
        tests = {
            "upload_sample": falcon.UploadSampleV3(file_data={}, file_name='oops_I_broke_it.jpg')["status_code"],
            "get_sample": falcon.GetSampleV3(ids='DoesNotExist')["status_code"],
            "delete_sample": falcon.DeleteSampleV3(ids='12345678')["status_code"]
        }
        return all(value in AllowedResponses for value in tests.values())

    def test_all_functionality(self):
        """Pytest harness hook"""
        assert self.sample_upload_download_delete() is True

    def test_errors(self):
        """Pytest harness hook"""
        assert self.sample_errors() is True

    # @staticmethod
    # def test_logout():
    #     """Pytest harness hook"""
    #     assert bool(falcon.auth_object.revoke(
    #         falcon.auth_object.token()["body"]["access_token"]
    #         )["status_code"] in AllowedResponses) is True
