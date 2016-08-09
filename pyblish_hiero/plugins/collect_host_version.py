import pyblish.api

import nuke


class CollectHostVersion(pyblish.api.ContextPlugin):
    """Inject the hosts version into context"""

    order = pyblish.api.CollectorOrder

    def process(self, context):

        context.set_data('hostVersion', value=nuke.NUKE_VERSION_STRING)
