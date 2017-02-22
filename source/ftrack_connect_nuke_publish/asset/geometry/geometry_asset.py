# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import nuke
import ftrack_connect_pipeline.asset


def filter_instances(pyblish_context):
    '''Return camera instances from *pyblish_context*.'''
    match = set(['geo', 'ftrack'])
    return filter(
        lambda instance: match.issubset(instance.data['families']),
        pyblish_context
    )


class PublishGeo(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of nuke geometry.'''

    in_place_location_name = 'ftrack.unmanaged'

    enable_in_place_location_publish = True

    def __init__(
        self, description, asset_type_short=None,
        enable_scene_as_reference=True,
        enable_reviewable_component=True
    ):
        super(PublishGeo, self).__init__(
            description, asset_type_short, True, False
        )

    def get_options(self):
        '''Return global options.'''
        options = []

        if self.enable_in_place_location_publish:
            options.append({
                'type': 'boolean',
                'name': 'publish_files_in_place',
                'label': 'In place publish',
                'value': False
            })

        default_options = super(PublishGeo, self).get_options()

        return default_options + options

    def get_publish_items(self):
        '''Return list of items that can be published.'''

        options = []
        for instance in filter_instances(self.pyblish_context):
            options.append({
                'label': instance.name,
                'name': instance.id,
                'value': instance.data.get('publish', False)
            })

        return options

    def update_with_options(
        self, item_options, general_options, selected_items
    ):
        '''Update *item_options* and *general_options*.'''
        super(PublishGeo, self).update_with_options(
            item_options, general_options, selected_items
        )
        self.logger.debug(
            'Updating nuke write geo nodes with "publish_files_in_place" '
            'option: {0!r}'.format(general_options['publish_files_in_place'])
        )

        if general_options['publish_files_in_place']:
            for instance in self.pyblish_context:
                if instance.data['families'] == ['ftrack', 'geo']:
                    instance.data['options']['location_name'] = (
                        self.in_place_location_name
                    )

    def get_scene_selection(self):
        '''Return a list of names for scene selection.'''
        selection = []
        for node in nuke.selectedNodes():
            selection.append(node.name())

        # Return list of instance ids for selected items in scene that match the
        # family.
        return [
            instance.id for instance in filter_instances(self.pyblish_context)
            if instance.name in selection
        ]
