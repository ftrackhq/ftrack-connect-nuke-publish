# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import nuke

registered_plugins = False


def register_pyblish_plugins():
    '''Register pyblish plugins.'''
    print 'REGISTER COMMON PLUGINS!'
    import ftrack_connect_nuke_publish
    import ftrack_connect_pipeline

    ftrack_connect_nuke_publish.register_shared_pyblish_plugins()
    ftrack_connect_pipeline.register_shared_pyblish_plugins()


def get_plugin_information():
    '''Return plugin information for nuke.'''
    import ftrack_connect_nuke_publish
    import ftrack_connect_nuke_publish._version
    return {
        'application_id': 'nuke',
        'plugin_version': ftrack_connect_nuke_publish._version.__version__
    }


def open_publish():
    '''Open publish dialog.'''
    import ftrack_connect_nuke_publish
    import ftrack_api

    session = ftrack_api.Session()
    session.event_hub.subscribe(
        'topic=ftrack.pipeline.get-plugin-information',
        lambda event: get_plugin_information()
    )

    ftrack_connect_nuke_publish.register_assets(session)

    global registered_plugins
    if registered_plugins is False:
        register_pyblish_plugins()
        registered_plugins = True

    import ftrack_connect_pipeline.ui.publish_actions_dialog
    ftrack_connect_pipeline.ui.publish_actions_dialog.show(session)


nukeMenu = nuke.menu('Nuke')
ftrackMenu = nukeMenu.addMenu('&ftrack new')
ftrackMenu.addCommand('Publish', open_publish)
