# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os

import pyblish.plugin
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


def register_shared_pyblish_plugins():
    '''Register shared pyblish plugins.'''
    # Register shared pyblish plugins.
    path = os.path.normpath(
        os.path.join(
            os.path.abspath(
                os.path.dirname(
                    __file__
                )
            ),
            'shared_pyblish_plugins'
        )
    )
    pyblish.plugin.register_plugin_path(path)
