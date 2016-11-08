# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import ftrack_api
import nuke
import ftrack_connect_pipeline.asset


class PublishCamera(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of nuke cameras.'''

    def get_options(self, publish_data):
        '''Return global options.'''
        options = []

        default_options = super(
            PublishCamera, self
        ).get_options(publish_data)

        options += default_options
        return options

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = []
        for instance in publish_data:
            if instance.data['family'] in ('ftrack.nuke.camera',):
                options.append(
                    {
                        'label': instance.name,
                        'name': instance.name,
                        'value': True
                    }
                )

        return options


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier='camera',
        publish_asset=PublishCamera(
            label='Camera',
            description='publish camera to ftrack.',
            icon='http://www.clipartbest.com/cliparts/LiK/dLB/LiKdLB6zT.png'
        )
    )

    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)
