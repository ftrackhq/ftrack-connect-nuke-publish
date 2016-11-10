# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import ftrack_connect_pipeline.asset


class PublishImageSequence(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of nuke image sequences.'''

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''

        options = []
        for instance in publish_data:
            if instance.data['family'] in (
                'ftrack.nuke.write', 'ftrack.nuke.script'
            ):
                options.append({
                    'label': instance.name,
                    'name': instance.name,
                    'value': True
                })

        return options
