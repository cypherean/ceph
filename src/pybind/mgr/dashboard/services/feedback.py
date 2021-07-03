# -*- coding: utf-8 -*-

import json
import logging
import os
from typing import Optional
from redminelib import Redmine

from requests.auth import AuthBase

from mgr_module import CLICommand

from ..settings import Settings
from ..exceptions import DashboardException
from ..rest_client import RestClient


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

    @RestClient.api_post('/issues', resp_structure='*')
    def create_issue(self, project_id, tracker_id, subject, description, category_id, severity, request=None):
        redmine = Redmine("https://tracker.ceph.com", key=self.get_api_key())
        project = redmine.project.get("Ceph")
        # ceph_project_id = project.id
        issue = redmine.issue.create(
            project_id=project_id,
            tracker_id=tracker_id,
            subject=subject,
            description=description,
            category_id=category_id,
            Severity=severity
        )
        return issue
        # response = request({
        #     "issue":
        #     {'project': project_id,
        #      'tracker': tracker_id,
        #      'subject': subject,
        #      'description': description,
        #      'category': category_id,
        #      'severity': severity}})
        # return response


class IssueModel:
    project_id: str
    tracker_id: str
    subject: str
    description: str
    category_id: str
    severity: str

    def __init__(self, project_id, tracker_id, subject, description, category_id, severity):
        self.project_id = project_id
        self.tracker_id = tracker_id
        self.subject = subject
        self.description = description
        self.category_id = category_id
        self.severity = severity

    def as_dict(self):
        return {'project_id': self.project_id,
                'subject': self.subject,
                'description': self.description,
                'category_id': self.category_id,
                'severity': self.severity}
