"""
test_scheduled_reports.py - This class tests the Scheduled Reports service class
"""
import os
import sys

# Authentication via the test_authorization.py
from tests import test_authorization as Authorization
# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# Classes to test - manually imported from sibling folder
from falconpy.report_executions import ReportExecutions

auth = Authorization.TestAuthorization()
token = auth.getConfigExtended()
falcon = ReportExecutions(access_token=token)
AllowedResponses = [200, 201, 403, 404, 429]  # Getting 403's atm


class TestIOC:
    def ioc_run_all_tests(self):
        tests = {
            "get_download": falcon.get_download(ids='12345678'),
            "get_reports": falcon.get_reports(ids='12345678'),
            "query_reports": falcon.query_reports(limit=1)
        }
        return all(
            value["status_code"] in AllowedResponses for value in tests.values()
        )

    def test_all_functionality(self):
        assert self.ioc_run_all_tests() is True
