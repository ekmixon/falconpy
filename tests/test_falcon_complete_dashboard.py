# test_falcon_complete_dashboard.py
# This class tests the falcon_complete_dashboard service class
import os
import sys

# Authentication via test_authorization.py
from tests import test_authorization as Authorization
# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# Classes to test - manually imported from sibling folder
from falconpy.falcon_complete_dashboard import Complete_Dashboard as FalconCD

auth = Authorization.TestAuthorization()
token = auth.getConfigExtended()
falcon = FalconCD(access_token=token)
AllowedResponses = [200, 403, 429]


class TestFalconCompleteDashboard:
    def ServiceFCD_QueryAllowListFilter(self):
        return falcon.QueryAllowListFilter()["status_code"] in AllowedResponses

    def ServiceFCD_QueryBlockListFilter(self):
        return falcon.QueryBlockListFilter()["status_code"] in AllowedResponses

    def ServiceFCD_QueryDetectionIdsByFilter(self):
        return (
            falcon.QueryDetectionIdsByFilter(bananas="yellow")["status_code"]
            in AllowedResponses
        )

    def ServiceFCD_GetDeviceCountCollectionQueriesByFilter(self):
        return (
            falcon.GetDeviceCountCollectionQueriesByFilter(
                parameters={"limit": 1}
            )["status_code"]
            in AllowedResponses
        )

    def ServiceFCD_QueryEscalationsFilter(self):
        return (
            falcon.QueryEscalationsFilter(limit=1, offset=2)["status_code"]
            in AllowedResponses
        )

    def ServiceFCD_QueryIncidentIdsByFilter(self):
        return (
            falcon.QueryIncidentIdsByFilter(bananas="yellow")["status_code"]
            in AllowedResponses
        )

    def ServiceFCD_QueryRemediationsFilter(self):
        return (
            falcon.QueryRemediationsFilter(bananas="yellow")["status_code"]
            in AllowedResponses
        )

    def ServiceFCD_GenerateErrors(self):
        falcon.base_url = "nowhere"
        errorChecks = True
        commandList = [
            ["AggregateAllowList", "body={}"],
            ["AggregateBlockList", "body=[{}]"],
            ["AggregateDetections", "body={}"],
            ["AggregateDeviceCountCollection", "body=[{}]"],
            ["AggregateEscalations", "body={}"],
            ["AggregateFCIncidents", "body=[{}]"],
            ["AggregateRemediations", "body={}"],

        ]
        for cmd in commandList:
            if eval(f"falcon.{cmd[0]}({cmd[1]})['status_code']") != 500:
                errorChecks = False

        return errorChecks

    def test_QueryAllowListFilter(self):
        assert self.ServiceFCD_QueryAllowListFilter() is True

    def test_QueryBlockListFilter(self):
        assert self.ServiceFCD_QueryBlockListFilter() is True

    def test_QueryDetectionIdsByFilter(self):
        assert self.ServiceFCD_QueryDetectionIdsByFilter() is True

    def test_GetDeviceCountCollectionQueriesByFilter(self):
        assert self.ServiceFCD_GetDeviceCountCollectionQueriesByFilter() is True

    def test_QueryEscalationsFilter(self):
        assert self.ServiceFCD_QueryEscalationsFilter() is True

    def test_QueryIncidentIdsByFilter(self):
        assert self.ServiceFCD_QueryIncidentIdsByFilter() is True

    def test_QueryRemediationsFilter(self):
        assert self.ServiceFCD_QueryRemediationsFilter() is True

    def test_Errors(self):
        assert self.ServiceFCD_GenerateErrors() is True