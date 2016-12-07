# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import functools

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_nuke_publish.asset.image_sequence import image_sequence_asset

FTRACK_ASSET_TYPE = 'img'


def create_asset_publish():
    '''Return asset publisher.'''
    return image_sequence_asset.PublishImageSequence(
        description='publish media to ftrack.',
        asset_type_short=FTRACK_ASSET_TYPE
    )


def register_asset_plugin(session, event):
    '''Register asset plugin.'''
    image_sequence = ftrack_connect_pipeline.asset.Asset(
        identifier=FTRACK_ASSET_TYPE,
        label='Media',
        icon='http://www.clipartbest.com/cliparts/9Tp/erx/9Tperxqrc.png',
        create_asset_publish=create_asset_publish
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_sequence.register(session)


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    session.event_hub.subscribe(
        'topic=ftrack.pipeline.register-assets',
        functools.partial(register_asset_plugin, session)
    )
