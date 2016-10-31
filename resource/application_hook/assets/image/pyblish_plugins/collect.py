import pyblish.api
import ftrack_connect_pipeline.util
import nuke


class FtrackPublishCollector(pyblish.api.ContextPlugin):
    '''Prepare ftrack publish.'''

    order = pyblish.api.CollectorOrder

    families = ['*']

    def process(self, context):
        '''Process *context* and add ftrack entity.'''
        ftrack_entity = ftrack_connect_pipeline.util.get_ftrack_entity()
        context.data['ftrack_entity'] = ftrack_entity


class CollectWriteNodes(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes from scene.'''

    order = pyblish.api.CollectorOrder

    families = ['ftrack.nuke.write']

    def process(self, context):
        '''Process *context* and add nuke write node instances.'''

        for node in nuke.allNodes():
            print "*** Collecting write nodes!!!"

            if node.Class() == 'Write':
                instance = context.create_instance(node.name(), family='ftrack.nuke.write')
                instance.data['publish'] = True
                instance.data['ftrack_components'] = []


pyblish.api.register_plugin(FtrackPublishCollector)
pyblish.api.register_plugin(CollectWriteNodes)
