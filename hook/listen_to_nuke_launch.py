# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os

import ftrack
import ftrack_connect.application

'''
    This connect plugin hook will add the pyblish nuke prototype to the
    environment when Nuke is launching from Connect. This hook should only
    be sourced by Connect.
'''


plugin_base_dir = os.path.normpath(
    os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ),
        '..'
    )
)

publish_actions_path = os.path.join(
    plugin_base_dir, 'resource', 'application_hook'
)

pyblish_plugin_path = os.path.join(
    plugin_base_dir, 'resource', 'pyblish_plugin'
)

nuke_plugin_path = os.path.join(
    plugin_base_dir, 'resource', 'nuke_plugin'
)

python_dependencies = os.path.join(
    plugin_base_dir, 'dependencies'
)


def on_application_launch(event):
    '''Handle application launch and add environment to *event*.'''
    ftrack_connect.application.appendPath(
        publish_actions_path,
        'FTRACK_EVENT_PLUGIN_PATH',
        event['data']['options']['env']
    )
    ftrack_connect.application.appendPath(
        python_dependencies,
        'PYTHONPATH',
        event['data']['options']['env']
    )
    ftrack_connect.application.appendPath(
        python_dependencies,
        'PYTHONPATH',
        event['data']['options']['env']
    )
    ftrack_connect.application.appendPath(
        pyblish_plugin_path,
        'PYBLISHPLUGINPATH',
        event['data']['options']['env']
    )
    ftrack_connect.application.appendPath(
        nuke_plugin_path,
        'NUKE_PATH',
        event['data']['options']['env']
    )
    event['data']['options']['env']['FTRACK_CONTEXT_ID'] = (
        event['data']['options']['env']['FTRACK_TASKID']
    )


def register(registry):
    '''Subscribe to application launch events on *registry*.'''
    if registry is not ftrack.EVENT_HANDLERS:
        # Not a session, let us early out to avoid registering multiple times.
        return

    #: TODO: Only apply when Nuke launches.
    ftrack.EVENT_HUB.subscribe(
        'topic=ftrack.connect.application.launch',
        on_application_launch
    )
