# # -*- coding: utf-8 -*-
import os
from collections import defaultdict

from .. import mgr
from ..services import feedback
from . import ApiController, ControllerDoc, RESTController
from mgr_module import CLICommand, CLIWriteCommand
from ..plugins import PLUGIN_MANAGER as PM


# Switch for python data class
FEEDBACK_SCHEMA = ([{
    # response
}], '')

@ApiController('/feedback', secure=False)
@ControllerDoc("Feedback API", "Report")
class Feedback(RESTController):
    issueAPIkey = None

    def __init__(self):  # pragma: no cover
        super(Feedback, self).__init__()
        self.cephTrackerClient = feedback.CephTrackerClient()


    def create(self, project_id, tracker_id, subject, description, category_id, severity):
        """
        Create an issue.
        :param component: The buggy ceph component.
        :param title: The title of the issue.
        :param description: The description of the issue.
        """
        return self.cephTrackerClient.create_issue(project_id, tracker_id, subject, description, category_id, severity)

    
    def get(self, issue_number):
        """
        Validate the issue tracker API given by user.
        :param issueAPI: The issue tracker API access key.
        """
        return self.cephTrackerClient.get_issues(issue_number)


# @PM.add_hook
# class CLI_Feedback():
#     @CLICommand('dashboard issue')
#     def cli_report_issue(self, project_id: int, tracker_id: int, subject: str, description: str, category_id: int, severity: str):
#         feedback = Feedback.create(project_id, tracker_id, subject, description, category_id, severity)
#         return (0, '', '')
