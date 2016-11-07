# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api
import tempfile


class IntegratorCreateNukeScriptComponent(pyblish.api.ContextPlugin):
    '''Create ftrack nukescript component if the used enabled it.'''

    order = pyblish.api.IntegratorOrder + 0.1

    def process(self, context):
        import nuke
        comment = context.data['options'].get(
            'comment_field', {}
        ).get('comment', 'No comment set')

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


pyblish.api.register_plugin(IntegratorCreateImageSequenceComponents)
pyblish.api.register_plugin(IntegratorCreateNukeScriptComponent)
