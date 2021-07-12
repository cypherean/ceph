# -*- coding: utf-8 -*-

import logging
from typing import Optional
from redminelib import Redmine
from enum import Enum
import errno

from requests.auth import AuthBase
from mgr_module import CLICommand
from mgr_module import CLIWriteCommand

from ..settings import Settings
from ..exceptions import DashboardException, ScopeNotInRole
from ..rest_client import RestClient
from ..plugins import PLUGIN_MANAGER as PM


class Feedback(Enum):
    project_id = 1,
    tracker_id = 1,
    subject = '',
    description = '',
    category_id = 195,
    Severity = '3 - Minor'



@CLICommand('issue create')
def cli_create_issue(self, project_id: int, tracker_id: int, subject: str, description: Optional[str] = None, category_id: Optional[str] = None, severity: Optional[str] = None, inbuf: Optional[str] = None):
    cephTrackerClient = CephTrackerClient()
    response = cephTrackerClient.create_issue(
        project_id, tracker_id, subject, description, category_id, severity)
    return 0, str[response], ''

@CLICommand('issue get')
def cli_create_issue(self, issue_number: int):
    cephTrackerClient = CephTrackerClient()
    response = cephTrackerClient.get_issues(issue_number=issue_number)
    return 0, str[response], ''

class RedmineAuth(AuthBase):
    def __init__(self, access_key):
        self.access_key = str(access_key)

    def __call__(self, r):
        r.headers['X-Redmine-API-Key'] = self.access_key
        return r


class CephTrackerClient(RestClient):
    access_key = ''

    def __init__(self):
        super().__init__('tracker.ceph.com', None, client_name='CephTracker',
                         ssl=True, auth=RedmineAuth(self.get_api_key()), ssl_verify=True)

    @staticmethod
    def get_api_key():
        try:
            access_key = Settings.CEPH_TRACKER_API_KEY
        except KeyError as error:
            raise DashboardException(msg='',
                                     http_status_code=404,
                                     component='')

        return access_key

    @RestClient.api_get('/issues/{issue_number}.json', resp_structure='*')
    def get_issues(self, issue_number, request=None):
        response = request()
        return response

    @CLICommand('dashboard feedback', perm='w')
    @RestClient.api_post('/issues', resp_structure='*')
    def create_issue(self, project_id: int, tracker_id: int, subject: str, description: str, category_id: int, severity: Optional[str] = '3 - Minor', inbuf: Optional[str] = None, request=None):
        '''
        Create an issue in the Ceph Issue tracker
        '''

        obj = self.find_object(project_id)
        if obj is None:
            return -errno.EEXIST, '', 'Project ID not found'
        redmine = Redmine("https://tracker.ceph.com", key=self.get_api_key())
        # project = redmine.project.get("Ceph")
        # issue = redmine.issue.create(
        #     project_id=project_id,
        #     tracker_id=tracker_id,
        #     subject=subject,
        #     description=description,
        #     category_id=category_id,
        #     Severity=severity
        # )
        return 1, '', ''
