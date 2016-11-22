# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import ftrack_api.event.base


def register_assets(session):
    '''Register by emitting event on *session*.'''

    # Emit event to register assets.
    session.event_hub.publish(
        ftrack_api.event.base.Event(
            topic='ftrack.pipeline.register-assets',
            data=dict()
        ),
        synchronous=True
    )

