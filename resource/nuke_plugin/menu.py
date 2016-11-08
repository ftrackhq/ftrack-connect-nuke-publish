# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import nuke


def get_plugin_information():
    '''Return plugin information for maya.'''
    import ftrack_connect_nuke_publish
    return {
        'application_id': 'nuke',
        'plugin_version': ftrack_connect_nuke_publish._version.__version__
    }


def open_publish():
    '''Open publish dialog.'''
    import ftrack_api

    session = ftrack_api.Session()
    session.event_hub.subscribe(
        'topic=ftrack.pipeline.get-plugin-information',
        lambda event: get_plugin_information()
    )

    import ftrack_connect_nuke_publish
    ftrack_connect_nuke_publish.register_assets(session)

    import ftrack_connect_pipeline.ui.publish_actions_dialog
    ftrack_connect_pipeline.ui.publish_actions_dialog.show(session)


nukeMenu = nuke.menu('Nuke')
ftrackMenu = nukeMenu.addMenu('&ftrack new')
ftrackMenu.addCommand('Publish', open_publish)
