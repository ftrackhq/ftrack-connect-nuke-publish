# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import nuke
import ftrack_connect_pipeline.asset


class PublishImageSequence(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of nuke image sequences.'''

    in_place_location_name = 'ftrack.unmanaged'

    enable_in_place_location_publish = True

    def get_options(self, publish_data):
        '''Return global options.'''
        options = []

        if self.enable_in_place_location_publish:
            options.append({
                'type': 'boolean',
                'name': 'publish_files_in_place',
                'label': 'In place publish',
                'value': False
            })

        default_options = super(
            PublishImageSequence, self
        ).get_options(publish_data)

        options += default_options
        return options

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = []
        for instance in publish_data:
            if instance.data['family'] in ('ftrack.nuke.write',):
                options.append({
                    'label': instance.name,
                    'name': instance.name,
                    'value': True
                })

        return options

    def update_with_options(
        self, publish_data, item_options, general_options, selected_items
    ):
        '''Update *publish_data* with *item_options* and *general_options*.'''
        super(PublishImageSequence, self).update_with_options(
            publish_data, item_options, general_options, selected_items
        )
        self.logger.debug(
            'Updating nuke write nodes with "publish_files_in_place" option: '
            '{0!r}'.format(general_options['publish_files_in_place'])
        )

        if general_options['publish_files_in_place']:
            for instance in publish_data:
                if instance.data['family'] in ('ftrack.nuke.write',):
                    instance.data['options']['location_name'] = (
                        self.in_place_location_name
                    )

    def get_scene_selection(self):
        '''Return a list of names for scene selection.'''
        selection = []
        for node in nuke.selectedNodes():
            selection.append(node.name())

        return selection
