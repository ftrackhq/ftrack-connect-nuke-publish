import ftrack_api

import ftrack_connect_pipeline.asset

import nuke

IDENTIFIER = 'image'


class PublishImage(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya image.'''

    def get_options(self, publish_data):
        '''Return global options.'''
        options = [{
            'type': 'group',
            'label': 'Nuke Media',
            'name': 'nuke_media',
            'options': [{
                'name': 'force_copy',
                'label': 'Force Copy Files',
                'type': 'boolean',
            }, {
                'name': 'attach_nuke_script',
                'label': 'Attach Nuke Script',
                'type': 'boolean',
            }]
        }]

        default_options = super(
            PublishImage, self
        ).get_options(publish_data)

        options += default_options
        return options

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''

        options = []
        for instance in publish_data:
            if instance.data['family'] in ('ftrack.nuke.write', ):
                options.append({
                    'label': instance.name,
                    'name': instance.id,
                    'value': True
                })

        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''
        options = []
        return options

    def get_scene_selection(self):
        '''Return a list of names for scene selection.'''
        names = []
        for node in nuke.allNodes():
            if node.Class() == 'Write':
                names.append(node.name())

        return names

def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishImage(
            label='Media',
            description='publish media to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9Tp/erx/9Tperxqrc.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)
