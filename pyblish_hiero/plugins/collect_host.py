import pyblish.api


class CollectHost(pyblish.api.ContextPlugin):
    """Inject the host into context"""

    order = pyblish.api.CollectorOrder

    def process(self, context):
        context.set_data("host", pyblish.api.current_host())
