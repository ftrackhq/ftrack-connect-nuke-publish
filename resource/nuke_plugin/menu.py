# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os

import nuke
import ftrack_connect_pipeline

import ftrack_connect_nuke_publish.plugin


plugin = ftrack_connect_nuke_publish.plugin.NukePlugin(
    context_id=os.environ['FTRACK_CONTEXT_ID']
)
ftrack_connect_pipeline.register_plugin(plugin)


nuke_menu = nuke.menu('Nuke')
ftrack_menu = nuke_menu.addMenu('&ftrack new')
ftrack_menu.addCommand('Publish', plugin.open_publish)
ftrack_menu.addCommand('Switch Context', plugin.open_switch_context)
