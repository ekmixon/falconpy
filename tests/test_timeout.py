# test_timeout.py
# This class tests request timeouts
import os
import sys

# Authentication via the test_authorization.py
from tests import test_authorization as Authorization
# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# Classes to test - manually imported from sibling folder
from falconpy.cloud_connect_aws import Cloud_Connect_AWS as FalconAWS
from falconpy.oauth2 import OAuth2 as FalconAuth

auth = Authorization.TestAuthorization()
auth.serviceAuth()

AllowedResponses = [200, 429, 500]  # Adding rate-limiting as an allowed response for now


class TestTimeouts:
    def timeout_test(self):
        falcon = FalconAWS(creds={
            'client_id': auth.config["falcon_client_id"],
            'client_secret': auth.config["falcon_client_secret"]
        })
        result = falcon.QueryAWSAccounts()
        return result['status_code'] in AllowedResponses

    def timeout_connect(self):
        falconConnectFail = FalconAWS(creds={
            'client_id': auth.config["falcon_client_id"],
            'client_secret': auth.config["falcon_client_secret"]
        }, timeout=(.001, 5)
        )
        result = falconConnectFail.QueryAWSAccounts()
        return (
            result['status_code'] in AllowedResponses
            and "connect timeout" in result["body"]["errors"][0]["message"]
        )

    def timeout_read(self):
        falconReadFail = FalconAWS(creds={
            'client_id': auth.config["falcon_client_id"],
            'client_secret': auth.config["falcon_client_secret"]
        }, timeout=(5, .001)
        )
        result = falconReadFail.QueryAWSAccounts()
        return (
            result['status_code'] in AllowedResponses
            and "read timeout" in result["body"]["errors"][0]["message"]
        )

    def timeout_standard(self):
        falconStandardFail = FalconAWS(creds={
            'client_id': auth.config["falcon_client_id"],
            'client_secret': auth.config["falcon_client_secret"]
        }, timeout=.001
        )
        result = falconStandardFail.QueryAWSAccounts()
        return (
            result['status_code'] in AllowedResponses
            and "connect timeout" in result["body"]["errors"][0]["message"]
        )

    def timeout_legacy_auth(self):
        falconLegacyFail = FalconAuth(creds={
            'client_id': auth.config["falcon_client_id"],
            'client_secret': auth.config["falcon_client_secret"]
        }, timeout=.001)
        result = falconLegacyFail.token()
        return (
            result["status_code"] in AllowedResponses
            and "connect timeout" in result["body"]["errors"][0]["message"]
        )

    def test_NoTimeout(self):
        assert self.timeout_test() is True

    def test_StandardTimeout(self):
        assert self.timeout_standard() is True

    def test_ConnectTimeout(self):
        assert self.timeout_connect() is True

    def test_ReadTimeout(self):
        assert self.timeout_read() is True

    def test_LegacyTimeout(self):
        assert self.timeout_legacy_auth() is True
