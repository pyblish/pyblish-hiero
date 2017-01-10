import pyblish.api

import hiero


class CollectSelection(pyblish.api.Contextplugin):
    """Inject the active project into context"""

    version = (0, 1, 0)
    order = pyblish.api.CollectorOrder - 0.1

    def process(self, context):

        if hasattr(hiero, 'selection'):
            context.set_data('selection', value=hiero.selection)
