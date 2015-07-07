# Dependencies
import pyblish_endpoint.service

import hiero

wrapper = hiero.core.executeInMainThreadWithResult


class HieroService(pyblish_endpoint.service.EndpointService):
    def init(self, *args, **kwargs):
        orig = super(HieroService, self).init
        return wrapper(orig, args, kwargs)

    def process(self, *args, **kwargs):
        orig = super(HieroService, self).process
        return wrapper(orig, args, kwargs)

    def repair(self, *args, **kwargs):
        orig = super(HieroService, self).repair
        return wrapper(orig, args, kwargs)
