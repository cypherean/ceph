# -*- coding: utf-8 -*-

import json
import logging
import os
from qa.tasks.radosgw_admin import main

from requests.auth import AuthBase

from pybind.mgr.dashboard.rest_client import RestClient

from .. import mgr
from ..settings import Settings
from ..exceptions import DashboardException
from ..rest_client import RestClient

class RedmineAuth(AuthBase):
    def __init__(self, access_key):
        self.access_key = str(access_key)

    def __call__(self, r):
        r.headers['X-Redmine-API-Key'] = self.access_key
        return r


class CephTrackerClient(RestClient):
    access_key = ''

    @staticmethod
    def get_api_key():
        try:
            access_key = Settings.CEPH_TRACKER_API_KEY
        except TypeError:
            # Legacy string values.
            access_key = Settings.CEPH_TRACKER_API_KEY
        except KeyError as error:
            raise DashboardException(msg='',
                                     http_status_code=404,
                                     component='')

        return access_key

    def __init__(self):
        super().__init__('https://tracker.ceph.com/issues/', 443, client_name='CephTracker',
                         ssl=True, auth=RedmineAuth(self.get_api_key()), ssl_verify=True)

    @RestClient.api_get('/{issue_number}.json', resp_structure='*')
    def get_issues(self, issue_number, request=None):
        response = request()
        return response

    @RestClient.api_post('/', resp_structure='*')
    def create_issue(self, subject, description, request=None):
        response = request({'project_id': 1,
                            'tracker_id': 1,
                            'subject': subject,
                            'description': description,
                            'category_id': '195',
                            'Severity': '3 - minor'})
        return response
