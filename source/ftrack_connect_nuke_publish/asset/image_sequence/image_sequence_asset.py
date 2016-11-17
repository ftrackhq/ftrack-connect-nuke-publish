# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import nuke
import ftrack_connect_pipeline.asset
import ftrack_connect_pipeline.pyblish


class PublishImageSequence(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of nuke image sequences.'''

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = []
        for instance in publish_data:
            if instance.data['family'] in (
                'ftrack.nuke.write',
            ):
                options.append({
                    'label': instance.name,
                    'name': instance.name,
                    'value': True
                })

        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''
        instance = ftrack_connect_pipeline.pyblish.get_instance(
            name, publish_data
        )
        if instance.data['family'] == 'ftrack.nuke.write':
            return [
                {
                    'type': 'text',
                    'name': 'component_name',
                    'label': 'Component name',
                    'value': instance.data['component_name']
                }
            ]

    def get_scene_selection(self):
        '''Return a list of names for scene selection.'''
        selection = []
        for node in nuke.selectedNodes():
            selection.append(node.name())

        return selection

    def get_options(self, publish_data):
        '''Return global options.'''
        options = [
            {
                'type': 'boolean',
                'name': 'attach_scene',
                'label': 'Attach scene for reference',
                'value': True
            }
        ]

        default_options = super(PublishImageSequence, self).get_options(
            publish_data
        )

        options += default_options
        return options
