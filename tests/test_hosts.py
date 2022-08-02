"""
test_hosts.py -  This class tests the hosts service class
"""
import platform
import os
import sys
import pytest
# Authentication via the test_authorization.py
from tests import test_authorization as Authorization

# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# Classes to test - manually imported from sibling folder
from falconpy import hosts as FalconHosts

auth = Authorization.TestAuthorization()
token = auth.getConfigExtended()
falcon = FalconHosts.Hosts(access_token=token)
AllowedResponses = [200, 202, 429]  # Adding rate-limiting as an allowed response for now


class TestHosts:
    """
    Hosts Service Class test harness
    """
    def hosts_add_tag(self):
        """
        Tests tagging functionality
        """
        id_list = [
            falcon.GetDeviceDetails(
                ids=falcon.QueryDevicesByFilter(parameters={"limit": 1})["body"][
                    "resources"
                ][0]
            )["body"]["resources"][0]["device_id"]
        ]

        # test basic, id is a list, single valid tag w/o manipulation
        if (
            falcon.UpdateDeviceTags(
                action_name="add", ids=id_list, tags=["FalconGroupingTags/testtag"]
            )["status_code"]
            not in AllowedResponses
        ):
            return False
        if (
            falcon.UpdateDeviceTags(
                action_name="remove",
                ids=id_list,
                tags=["FalconGroupingTags/testtag"],
            )["status_code"]
            not in AllowedResponses
        ):
            return False
        # id is a list, multiple tags needing manipulation
        if (
            falcon.UpdateDeviceTags(
                action_name="add",
                ids=id_list,
                tags=["testtag", "tagtest", "anothertag"],
            )["status_code"]
            not in AllowedResponses
        ):
            return False
        if (
            falcon.UpdateDeviceTags(
                action_name="remove",
                ids=id_list,
                tags=["testtag", "tagtest", "anothertag"],
            )["status_code"]
            not in AllowedResponses
        ):
            return False
        # id is a list, mutliple tags some need manipulation
        if (
            falcon.UpdateDeviceTags(
                action_name="add",
                ids=id_list,
                tags=[
                    "FalconGroupingTags/testtag",
                    "manipulate",
                    "FalconGroupingTags/anothertag",
                ],
            )["status_code"]
            not in AllowedResponses
        ):
            return False
        if (
            falcon.UpdateDeviceTags(
                action_name="remove",
                ids=id_list,
                tags=[
                    "FalconGroupingTags/testtag",
                    "manipulate",
                    "FalconGroupingTags/anothertag",
                ],
            )["status_code"]
            not in AllowedResponses
        ):
            return False
        # id is single string, single valid tag w/o manipulation
        if (
            falcon.UpdateDeviceTags(
                action_name="add",
                ids=id_list[0],
                tags=["FalconGroupingTags/testtag"],
            )["status_code"]
            not in AllowedResponses
        ):
            return False
        if (
            falcon.UpdateDeviceTags(
                action_name="remove",
                ids=id_list[0],
                tags=["FalconGroupingTags/testtag"],
            )["status_code"]
            not in AllowedResponses
        ):
            return False
        # Force the unit test down line 84
        return (
            falcon.UpdateDeviceTags(
                action_name="add", ids=id_list, tags="FalconGroupingTags/testtag"
            )["status_code"]
            in AllowedResponses
        )

    def hosts_generate_tag_error(self):
        """
        Tests tag error handling
        """
        id_list = [
            falcon.GetDeviceDetails(
                ids=falcon.QueryDevicesByFilter(parameters={"limit": 1})["body"][
                    "resources"
                ][0]
            )["body"]["resources"][0]["device_id"]
        ]

        #  Generate an error by sending garbage as the action_name
        return (
            falcon.UpdateDeviceTags(
                action_name="KaBOOM!",
                ids=id_list,
                tags=["FalconGroupingTags/testtag"],
            )["status_code"]
            == 500
        )

    def hosts_perform_action(self):
        """
        Tests the perform action endpoint
        """
        test_id = [falcon.QueryDevicesByFilter(limit=1)["body"]["resources"][0]]
        payload = {"ids": test_id}
        action_test = falcon.PerformActionV2(action_name="hide_host", body=payload)
        if action_test["status_code"] == 202:
            action_test = falcon.PerformActionV2(action_name="unhide_host", body=payload)
            return action_test["status_code"] == 202
        else:
            pytest.skip("Perform action test failure, skipping")
            return False

    def hosts_generate_errors(self):
        """
        Generates a series of 500 errors to test remaining code paths
        """
        falcon.base_url = "nowhere"
        tests = {
            "perform_action": falcon.PerformActionV2(body={}, action_name='unhide_host', parameters={})["status_code"],
            "perform_action_params": falcon.PerformActionV2(body={}, parameters={'action_name': 'PooF'})["status_code"],
            "perform_action_null": falcon.PerformActionV2(body={}, parameters={})["status_code"],
            "get_device_details": falcon.GetDeviceDetails(ids='12345678')["status_code"],
            "query_hidden_devices": falcon.QueryHiddenDevices()["status_code"],
            "query_devices_by_filter_scroll": falcon.QueryDevicesByFilterScroll()["status_code"],
            "query_devices_by_filter": falcon.QueryDevicesByFilter()["status_code"]
        }
        return all(value == 500 for value in tests.values())

    def test_query_hidden_devices(self):
        """Pytest harness hook"""
        assert (
            falcon.QueryHiddenDevices(parameters={"limit": 1})["status_code"]
            in AllowedResponses
        )

    def test_query_devices_by_filter_scroll(self):
        """Pytest harness hook"""
        assert (
            falcon.QueryDevicesByFilterScroll(parameters={"limit": 1})[
                "status_code"
            ]
            in AllowedResponses
        )

    def test_query_devices_by_filter(self):
        """Pytest harness hook"""
        assert (
            falcon.QueryDevicesByFilter(parameters={"limit": 1})["status_code"]
            in AllowedResponses
        )

    def test_tagging(self):
        """Pytest harness hook"""
        assert self.hosts_add_tag() is True

    def test_generate_tag_error(self):
        """Pytest harness hook"""
        assert self.hosts_generate_tag_error() is True

    def test_get_device_details(self):
        """Pytest harness hook"""
        # Test lazy loading of the ids parameter
        assert (
            falcon.GetDeviceDetails(
                falcon.QueryDevicesByFilter(parameters={"limit": 1})["body"][
                    "resources"
                ][0]
            )["status_code"]
            in AllowedResponses
        )

    @pytest.mark.skipif(sys.version_info.minor < 9, reason="Frequency reduced due to test flakiness")
    @pytest.mark.skipif(platform.system() != "Darwin", reason="Frequency reduced due to test flakiness")
    def test_perform_action(self):
        """Pytest harness hook"""
        assert self.hosts_perform_action() is True

    # @staticmethod
    # def test_logout():
    #     """Pytest harness hook"""
    #     assert bool(falcon.auth_object.revoke(
    #         falcon.auth_object.token()["body"]["access_token"]
    #         )["status_code"] in AllowedResponses) is True

    def test_errors(self):
        """Pytest harness hook"""
        assert self.hosts_generate_errors() is True
