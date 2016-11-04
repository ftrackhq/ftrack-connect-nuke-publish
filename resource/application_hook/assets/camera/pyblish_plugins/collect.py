# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import pyblish.api
import ftrack_connect_pipeline.util


class FtrackPublishCollector(pyblish.api.ContextPlugin):
    '''Prepare ftrack publish.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add ftrack entity.'''
        ftrack_entity = ftrack_connect_pipeline.util.get_ftrack_entity()
        context.data['ftrack_entity'] = ftrack_entity


class CollectCameras(pyblish.api.ContextPlugin):

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        import nuke

        for node in nuke.allNodes():
            if node.Class() == 'Camera' or node.Class() == 'Camera2':
                instance = context.create_instance(
                    node.name(), family='ftrack.nuke.camera'
                )

                instance.data['publish'] = True
                instance.data['ftrack_components'] = []


pyblish.api.register_plugin(FtrackPublishCollector)
pyblish.api.register_plugin(CollectCameras)
