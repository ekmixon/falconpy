"""
test_d4c_registration.py - This class tests the Discover for Cloud registration service class
"""
import os
import sys
# Authentication via test_authorization.py
from tests import test_authorization as Authorization
# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# Classes to test - manually imported from sibling folder
from falconpy.d4c_registration import D4C_Registration as FalconD4C

auth = Authorization.TestAuthorization()
token = auth.getConfigExtended()
falcon = FalconD4C(access_token=token)
AllowedResponses = [200, 429, 404]


class TestD4CRegistration:
    """
    Test harness for the D4C Registration Service Class
    """
    def d4c_get_azure_user_scripts_attachment(self):
        """
        get_azure_user_scripts_attachment
        """
        result = falcon.GetCSPMAzureUserScriptsAttachment()
        return (
            not isinstance(result, (bytes))
            and "status_code" in result
            and result["status_code"] in AllowedResponses
            or isinstance(result, (bytes))
        )

    def d4c_get_azure_user_scripts(self):
        """
        get_azure_user_scripts
        """
        result = falcon.GetCSPMAzureUserScripts()
        return (
            not isinstance(result, (bytes))
            and "status_code" in result
            and result["status_code"] in AllowedResponses
            or isinstance(result, (bytes))
        )

    def d4c_get_gcp_user_scripts_attachment(self):
        """
        get_gcp_user_scripts_attachment
        """
        result = falcon.GetCSPMGCPUserScriptsAttachment()
        return (
            not isinstance(result, (bytes))
            and "status_code" in result
            and result["status_code"] in AllowedResponses
            or isinstance(result, (bytes))
        )

    def d4c_get_gcp_user_scripts(self):
        """
        get_gcp_user_scripts
        """
        result = falcon.GetCSPMGCPUserScripts()
        return (
            not isinstance(result, (bytes))
            and "status_code" in result
            and result["status_code"] in AllowedResponses
            or isinstance(result, (bytes))
        )

    def d4c_generate_errors(self):
        """
        Test every code path within every method by generating 500s, does not hit the API
        """
        falcon.base_url = "nowhere"
        tests = {
            "get_azure_account": falcon.GetCSPMAzureAccount(ids='12345678', scan_type='dry')["status_code"],
            "update_azure_account_client_id": falcon.UpdateCSPMAzureAccountClientID(ids='12345678')["status_code"],
            "get_cgp_account": falcon.GetCSPMCGPAccount(ids='12345678', parameters={'scan_type': 'dry'})["status_code"],
            "get_gcp_acocunt": falcon.GetCSPMGCPAccount(ids='12345678')["status_code"],  # Test the typo fix version
            "create_gcp_account": falcon.CreateCSPMGCPAccount(body={})["status_code"],
            "create_azure_account": falcon.CreateCSPMAzureAccount(body={})["status_code"]
        }
        return all(value == 500 for value in tests.values())

    def test_GetCSPMAzureUserScriptsAttachment(self):
        """
        Pytest harness hook
        """
        assert self.d4c_get_azure_user_scripts_attachment() is True

    def test_GetCSPMAzureUserScripts(self):
        """
        Pytest harness hook
        """
        assert self.d4c_get_azure_user_scripts() is True

    def test_GetCSPMGCPUserScriptsAttachment(self):
        """
        Pytest harness hook
        """
        assert self.d4c_get_gcp_user_scripts_attachment() is True

    def test_GetCSPMGCPUserScripts(self):
        """
        Pytest harness hook
        """
        assert self.d4c_get_gcp_user_scripts() is True

    def test_Errors(self):
        """
        Pytest harness hook
        """
        assert self.d4c_generate_errors() is True

    # @staticmethod
    # def test_logout():
    #     """
    #     Pytest harness hook
    #     """
    #     assert bool(falcon.auth_object.revoke(
    #         falcon.auth_object.token()["body"]["access_token"]
    #         )["status_code"] in AllowedResponses) is True
