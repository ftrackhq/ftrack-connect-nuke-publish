import nuke

import ftrack_api
import ftrack_connect_pipeline.asset

session = ftrack_api.Session()


def open_publish():
    '''Open publish dialog.'''
    import ftrack_connect_pipeline.ui.publish_actions_dialog
    ftrack_connect_pipeline.ui.publish_actions_dialog.show(session)


nukeMenu = nuke.menu('Nuke')
ftrackMenu = nukeMenu.addMenu('&ftrack new')
ftrackMenu.addCommand('Publish', open_publish)
