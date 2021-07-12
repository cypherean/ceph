# from . import PLUGIN_MANAGER as PM
# from . import interfaces as I
# from .plugin import SimplePlugin as SP
# from enum import Enum
# from mgr_module import CLICommand, Option
# from typing import List, Optional, Set, no_type_check

# import cherrypy


# class Projects(Enum):
#     DASHBOARD = 1


# class Tracker(Enum):
#     BUG = 1
#     FEATURE = 5

# # Feature2Controller = {
# #     Projects: [project_id, tracker_id, ]
# # }

# @PM.add_plugin
# class Feedback(SP,I.HasCommands, I.FilterRequest.BeforeHandler):
#     OPTIONS = [
#         SP.Option('project_id', default=1, type='int'),
#         SP.Option('tracker_id', default=1, type='int'),
#         SP.Option('subject', default='', type='str'),
#         SP.Option('description', default='', type='str'),
#         SP.Option('category_id', default=195, type='int'),
#         SP.Option('severity', default='3 - Minor', type='str'),
#     ]

#     def report_issue(self):
#         return 0

#     @PM.add_hook
#     def register_commands(self):
#         @CLICommand("dashboard issue")
#         def cmd(mgr,
#                 project: Optional[List[Projects]] = None,
#                 tracker: Optional[List[Tracker]] = None):
#             '''
#             Report issue in Ceph Dashboard
#             '''
#             ret = 0
#             msg = []
#             if project is not None:
#                 if tracker is None:
#                     ret = 1
#                     msg = ["At least one tracker must be specified"]
#                 else:
#                     pass
#             else:
#                 ret = 1
#                 msg = ["At least one project must be specified"]
#             return ret, '\n'.join(msg), ''
#         return {'handle_command': cmd}

#     # @PM.add_hook
#     # def setup(self):
#     #   self.mute = self.get_option('mute')

#     # @PM.add_hook
#     # def filter_request_before_handler(self, request):
#     #   if self.mute:
#     #     raise cherrypy.HTTPError(500, "I'm muted :-x")

