# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import nuke
import ftrack_connect_pipeline.asset


class PublishCamera(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of nuke cameras.'''

    def get_options(self):
        '''Return global options.'''
        from ftrack_connect_pipeline.ui.widget.field import start_end_frame
        first = int(nuke.root().knob('first_frame').value())
        last = int(nuke.root().knob('last_frame').value())

        frame_range = start_end_frame.StartEndFrameField(first, last)

        options = [
            {
                'type': 'qt_widget',
                'name': 'frame_range',
                'widget': frame_range,
                'value': {
                    'start_frame': first,
                    'end_frame': last
                }
            }
        ]

        default_options = super(PublishCamera, self).get_options()

        return default_options + options

    def get_publish_items(self):
        '''Return list of items that can be published.'''
        match = set(['camera', 'ftrack'])

        options = []
        for instance in self.pyblish_context:
            if match.issubset(instance.data['families']):
                options.append(
                    {
                        'label': instance.name,
                        'name': instance.name,
                        'value': instance.data.get('publish', False)
                    }
                )

        return options

    def get_scene_selection(self):
        '''Return a list of names for scene selection.'''
        selection = []
        for node in nuke.selectedNodes():
            selection.append(node.name())

        return selection
