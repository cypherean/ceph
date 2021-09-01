
"""
Feedback module

See doc/mgr/feedback.rst for more info.
"""

from mgr_module import CLIReadCommand, HandleCommandResult, MgrModule, Option
from threading import Event
from typing import cast, Any, Optional, TYPE_CHECKING
import errno
from .services.feedback import CephTrackerClient
from .model.feedback import Feedback

class FeedbackModule(MgrModule):

    # there are CLI commands we implement
    @CLIReadCommand('set issue_key')
    def set_api_key(self, key: str) -> HandleCommandResult:
        """
        Set Ceph Issue Tracker API key
        """
        try:
            self.set_store('issue_tracker', key)
        except Exception as error:
            return HandleCommandResult(stderr=f'Exception in setting API key : {error}')
        return HandleCommandResult(stdout="Successfully updated key")

    @CLIReadCommand('get issue_key')
    def get_api_key(self) -> HandleCommandResult:
        """
        Get Ceph Issue Tracker API key
        """
        try:
            key = self.get_store('issue_tracker')
            if key is None:
                return HandleCommandResult(stderr='Issue tracker key is not set. Set key with `ceph set issue_key <your_key>`')
        except Exception as error:
            return HandleCommandResult(stderr=f'Error in retreiving issue tracker API key: {error}')
        return HandleCommandResult(stdout=f'Your key: {key}')

    @CLIReadCommand('get issue')
    def get_issue(self, issue_number: int) -> HandleCommandResult:
        """
        Fetch an issue
        """
        try:
            issue_number = int(issue_number)
        except TypeError:
            return -errno.EINVAL, '', f'Invalid issue number {issue_number}'
        cephTrackerClient = CephTrackerClient()
        try:
            response = cephTrackerClient.get_issues(issue_number)
        except FileNotFoundError:
            return HandleCommandResult(stderr=f'Issue number {issue_number} does not exist')
        except Exception:
            return HandleCommandResult(stderr="Error occured. Try again later")
        return HandleCommandResult(stdout=str(response))

    @CLIReadCommand('create issue')
    def create_issue(self, project: str, tracker: str, subject: str, description: str) -> HandleCommandResult:
        """
        Create an issue
        """
        try:
            feedback = Feedback(Feedback.Project[project].value,
                                Feedback.TrackerType[tracker].value, subject, description)
        except KeyError:
            return -errno.EINVAL, '', 'Invalid arguments'
        try:
            access_key = self.get_store('issue_tracker')
            if access_key is None:
                return HandleCommandResult(stderr='Issue tracker key is not set. Set key with `ceph set issue_key <your_key>`')
        except Exception as error:
            return HandleCommandResult(stderr=f'Error in retreiving issue tracker API key: {error}')
        tracker_client = CephTrackerClient()
        try:
            response = tracker_client.create_issue(feedback, access_key)
        except Exception as error:
            return HandleCommandResult(stderr=f'Error in creating issue: {str(error)}')
        return HandleCommandResult(stdout=str(response))
