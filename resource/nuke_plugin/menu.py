import nuke


def open_publish():
    import ftrack_api

    session = ftrack_api.Session()
    import ftrack_connect_pipeline.ui.publish_actions_dialog
    ftrack_connect_pipeline.ui.publish_actions_dialog.show(session)


nukeMenu = nuke.menu('Nuke')
ftrackMenu = nukeMenu.addMenu('&ftrack new')
ftrackMenu.addCommand('Publish', open_publish)
