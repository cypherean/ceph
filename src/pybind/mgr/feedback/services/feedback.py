# -*- coding: utf-8 -*-

import json

import requests
# from requests.auth import AuthBase

from ..model.feedback import Feedback
# from ...dashboard.rest_client import RestClient
# from ...dashboard.settings import Settings


class config:
    url = 'tracker.ceph.com'
    port = 443


# class RedmineAuth(AuthBase):
#     def __init__(self):
#         try:
#             self.access_key = Settings.ISSUE_TRACKER_API_KEY
#         except KeyError:
#             self.access_key = None

#     def __call__(self, r):
#         r.headers['X-Redmine-API-Key'] = self.access_key
#         return r


class CephTrackerClient:

    def get_issues(self, issue_number):
        '''
        Fetch an issue from the Ceph Issue tracker
        '''
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.get(
            f'https://tracker.ceph.com/issues/{issue_number}.json', headers=headers)
        if not response.ok:
            if response.status_code == 404:
                raise FileNotFoundError
            raise Exception(response.status_code)
        return {"message": response.text}

    def create_issue(self, feedback: Feedback, access_key: str):
        '''
        Create an issue in the Ceph Issue tracker
        '''
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-Redmine-API-Key': access_key,
            }
        except KeyError:
            raise Exception("Ceph Tracker API Key not set")
        data = json.dumps(feedback.as_dict())
        response = requests.post(
            f'https://tracker.ceph.com/projects/{feedback.project_id}/issues.json',
            headers=headers, data=data)
        if not response.ok:
            if response.status_code == 401:
                raise Exception("Unauthorized. Invalid Issue tracker API key")
            raise Exception(response.raise_for_status())
        return {"message": response.text}
