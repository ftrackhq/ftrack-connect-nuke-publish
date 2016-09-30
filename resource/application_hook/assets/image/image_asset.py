import ftrack_api

import ftrack_connect_pipeline.asset

IDENTIFIER = 'image'


class PublishImage(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya image.'''

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = []
        for instance in publish_data:
            if instance.data['family'] in ('write', ):
                options.append({
                    'label': instance.name,
                    'name': instance.id,
                    'value': True
                })

        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''
        print 'item', name
        for instance in publish_data:
            if instance.id == name:
                return [{
                    'type': 'text',
                    'label': 'Path',
                    'name': 'path',
                    'value': instance.data['options'].get('path')
                }]

        return []


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
