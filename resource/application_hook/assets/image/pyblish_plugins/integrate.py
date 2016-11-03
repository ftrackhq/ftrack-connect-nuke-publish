# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api
import nuke
import tempfile


class IntegratorCreateAsset(pyblish.api.ContextPlugin):
    '''Create asset and prepare publish.'''

    order = pyblish.api.IntegratorOrder

    def process(self, context):
        '''Process *context* create asset.'''

        ftrack_entity = context.data['ftrack_entity']
        session = ftrack_entity.session

        asset_type_id = context.data['options']['asset']['asset_type']
        asset_name = context.data['options']['asset']['asset_name']
        context_id = ftrack_entity['id']

        asset = session.query(
            'Asset where context_id is "{0}" and name is "{1}" and '
            'type_id is "{2}"'.format(
                context_id, asset_name, asset_type_id
            )
        ).first()

        if asset is None:
            asset = session.create(
                'Asset',
                {
                    'context_id': context_id,
                    'type_id': asset_type_id,
                    'name': asset_name
                }
            )

        # Create an asset version in a pre-published state.
        asset_version = session.create(
            'AssetVersion',
            {
                'asset': asset,
                'is_published': False
            }
        )

        session.commit()
        context.data['asset_version'] = asset_version


class IntegratorCreateImageSequenceComponents(pyblish.api.InstancePlugin):
    '''Create ftrack components.'''

    order = pyblish.api.IntegratorOrder + 0.1

    families = ['ftrack.nuke.write']

    def process(self, instance):
        '''Process *instance* and create components.'''

        import ftrack_api.symbol
        context = instance.context
        asset_version = context.data['asset_version']
        session = asset_version.session
        location = session.pick_location()
        comment = context.data['options'].get('comment_field', {}).get('comment', 'No comment set')

        for component_item in instance.data.get('ftrack_components', []):
            component_name = component_item['component_name']

            start = int(float(component_item['first']))
            end = int(float(component_item['last']))

            if start != end:
                sequence_path = u'{0} [{1}-{2}]'.format(
                    component_item['file_path'], start, end
                )
            else:
                sequence_path = unicode(component_item['file_path'] % start)

            session.create_component(
                sequence_path,
                {
                    'version_id': asset_version['id'],
                    'name': component_item['component_name'],
                    'comment': comment
                },
                location=location
            )

        session.commit()


class IntegratorCreateNukeScriptComponent(pyblish.api.ContextPlugin):
    '''Create ftrack nukescript component if the used enabled it.'''

    order = pyblish.api.IntegratorOrder + 0.1

    def process(self, context):

        comment = context.data['options'].get('comment_field', {}).get('comment', 'No comment set')
        context_options = context.data['options'].get('nuke_media', {})

        if context_options.get('attach_nuke_script', False):
            import ftrack_api.symbol
            asset_version = context.data['asset_version']
            session = asset_version.session
            location = session.pick_location()

            nukescript_path = ''
            if nuke.Root().name() == 'Root':
                tmp_script = tempfile.NamedTemporaryFile(suffix='.nk')
                nuke.scriptSaveAs(tmp_script.name)
                nukescript_path = tmp_script.name
            else:
                nukescript_path = nuke.root()['name'].value()

            session.create_component(
                nukescript_path,
                {
                    'version_id': asset_version['id'],
                    'name': 'nukescript',
                    'comment': comment
                },
                location=location
            )

            session.commit()


class IntegratorPublishVersion(pyblish.api.ContextPlugin):
    '''Mark asset version as published.'''

    order = pyblish.api.IntegratorOrder + 0.2

    def process(self, context):
        '''Process *context*.'''

        asset_version = context.data['asset_version']
        session = asset_version.session

        asset_version['is_published'] = True
        session.commit()


pyblish.api.register_plugin(IntegratorCreateAsset)
pyblish.api.register_plugin(IntegratorCreateImageSequenceComponents)
pyblish.api.register_plugin(IntegratorCreateNukeScriptComponent)
pyblish.api.register_plugin(IntegratorPublishVersion)
