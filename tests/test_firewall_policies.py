# test_firewall_policies.py
# This class tests the firewall_policies service class
import os
import sys
# Authentication via the test_authorization.py
from tests import test_authorization as Authorization
# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# flake8: noqa=R0402  # Classes to test - manually imported from sibling folder
from falconpy import firewall_policies as FalconFirewallPolicy

auth = Authorization.TestAuthorization()
token = auth.getConfigExtended()
falcon = FalconFirewallPolicy.Firewall_Policies(access_token=token)
AllowedResponses = [200, 429]  # Adding rate-limiting as an allowed response for now


class TestFirewallPolicy:

    def serviceFirewall_queryFirewallPolicies(self):
        return (
            falcon.queryFirewallPolicies(parameters={"limit": 1})["status_code"]
            in AllowedResponses
        )

    def serviceFirewall_GenerateErrors(self):
        falcon.base_url = "nowhere"
        errorChecks = True
        commandList = [
            ["queryCombinedFirewallPolicyMembers", ""],
            ["queryCombinedFirewallPolicies", ""],
            ["performFirewallPoliciesAction", "action_name='enable', body={}, parameters={}"],
            ["performFirewallPoliciesAction", "body={}, parameters={'action_name':'PooF'}"],
            ["performFirewallPoliciesAction", "body={}, parameters={}"],
            ["setFirewallPoliciesPrecedence", "body={}"],
            ["getFirewallPolicies", "ids='12345678'"],
            ["createFirewallPolicies", "body={}"],
            ["deleteFirewallPolicies", "ids='12345678'"],
            ["updateFirewallPolicies", "body={}"],
            ["queryFirewallPolicyMembers", ""],
            ["queryFirewallPolicies", ""]
        ]
        for cmd in commandList:
            if eval(f"falcon.{cmd[0]}({cmd[1]})['status_code']") != 500:
                errorChecks = False

        return errorChecks

    def test_Errors(self):
        assert self.serviceFirewall_GenerateErrors() is True
