# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import ftrack_api
import ftrack_connect_pipeline.asset
import nuke


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


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_sequence_asset = ftrack_connect_pipeline.asset.Asset(
        identifier='image_sequence',
        publish_asset=PublishImageSequence(
            label='Media',
            description='publish media to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9Tp/erx/9Tperxqrc.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_sequence_asset.register(session)
