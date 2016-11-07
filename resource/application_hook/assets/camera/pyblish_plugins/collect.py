# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import pyblish.api


class CollectCameras(pyblish.api.ContextPlugin):

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        import nuke

        self.log.debug('Started collecting camera from scene.')

        for node in nuke.allNodes():
            if node.Class() == 'Camera' or node.Class() == 'Camera2':
                instance = context.create_instance(
                    node.name(), family='ftrack.nuke.camera'
                )

                instance.data['publish'] = True
                instance.data['ftrack_components'] = []


pyblish.api.register_plugin(CollectCameras)
