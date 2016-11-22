# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api


class CollectNukeScript(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes from scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add nuke write node instances.'''
        self.log.debug('Started collecting scene script.')

        instance = context.create_instance(
            'Script', family='ftrack.nuke.script'
        )
        instance.data['publish'] = True
        instance.data['ftrack_components'] = []

        self.log.debug(
            'Collected Script instance {0!r}.'.format(
                instance
            )
        )