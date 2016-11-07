# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api
import nuke


class CollectWriteNodes(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes from scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add nuke write node instances.'''

        self.log.debug('Started collecting write nodes from scene.')

        for node in nuke.allNodes():
            if node.Class() == 'Write':
                instance = context.create_instance(
                    node.name(), family='ftrack.nuke.write'
                )
                instance.data['publish'] = True
                instance.data['ftrack_components'] = []


pyblish.api.register_plugin(CollectWriteNodes)
