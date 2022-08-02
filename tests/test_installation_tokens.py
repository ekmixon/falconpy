# test_installation_tokens.py
# This class tests the installation_tokens service class
import os
import sys

# Authentication via test_authorization.py
from tests import test_authorization as Authorization
# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# Classes to test - manually imported from sibling folder
from falconpy.installation_tokens import Installation_Tokens as FalconIT

auth = Authorization.TestAuthorization()
token = auth.getConfigExtended()
falcon = FalconIT(access_token=token)
AllowedResponses = [200, 429]


class TestInstallationTokens:
    def serviceIT_GetCustomerSettings(self):
        return falcon.customer_settings_read()["status_code"] in AllowedResponses

    def serviceIT_QueryAuditEvents(self):
        return (
            falcon.audit_events_query(limit=1, offset=2)["status_code"]
            in AllowedResponses
        )

    def serviceIT_QueryTokens(self):
        return (
            falcon.tokens_query(
                bananas="yellow", limit=1, parameters={"offset": 2}
            )["status_code"]
            in AllowedResponses
        )

    def serviceIT_GenerateErrors(self):
        falcon.base_url = "nowhere"
        errorChecks = True
        commandList = [
            ["audit_events_read", "ids='12345678'"],
            ["tokens_read", "ids='12345678'"],
            ["tokens_delete", "ids='12345678'"],
            ["tokens_update", "body={}, ids='12345678'"],
            ["tokens_create", "body={}"]
        ]
        for cmd in commandList:
            if eval(f"falcon.{cmd[0]}({cmd[1]})['status_code']") != 500:
                errorChecks = False

        return errorChecks

    def test_GetCustomerSettings(self):
        assert self.serviceIT_GetCustomerSettings() is True

    def test_QueryAuditEvents(self):
        assert self.serviceIT_QueryAuditEvents() is True

    def test_QueryTokens(self):
        assert self.serviceIT_QueryTokens() is True

    def test_Errors(self):
        assert self.serviceIT_GenerateErrors() is True
