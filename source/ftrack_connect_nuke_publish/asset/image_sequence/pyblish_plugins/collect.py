# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api


class CollectWriteNodes(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes from scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add nuke write node instances.'''
        import nuke
        self.log.debug('Started collecting write nodes from scene.')

        for node in nuke.allNodes():
            if node.Class() == 'Write':
                instance = context.create_instance(
                    node.name(), family='ftrack.nuke.write'
                )
                instance.data['publish'] = True
                instance.data['ftrack_components'] = []

                self.log.debug(
                    'Collected Write node instance {0!r} {1!r}.'.format(
                        node.name(), instance
                    )
                )


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
