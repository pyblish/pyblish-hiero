import pyblish.api

import hiero


@pyblish.api.log
class SelectCurrentFile(pyblish.api.Selector):
    """Inject the current working file into context"""

    version = (0, 1, 0)

    def process(self, context):
        """Todo, inject the current working file"""

        project = hiero.ui.activeView().selection()[0].project()

        context.set_data('currentFile', value=project.path())
