# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api
import tempfile


class ExtractNukeScriptComponent(pyblish.api.InstancePlugin):
    '''Create ftrack nukescript component if the used enabled it.'''

    order = pyblish.api.ExtractorOrder
    families = ['ftrack.nuke.script']

    def process(self, instance):

        self.log.debug(
            'Started extracting nuke script {0!r}'.format(
                instance.name
            )
        )

        import nuke
        nukescript_path = ''
        if nuke.Root().name() == 'Root':
            tmp_script = tempfile.NamedTemporaryFile(suffix='.nk')
            nuke.scriptSaveAs(tmp_script.name)
            nukescript_path = tmp_script.name
        else:
            nukescript_path = nuke.root()['name'].value()

        new_component = {
            'path': nukescript_path,
            'name': instance.name,
        }

        instance.data['ftrack_components'].append(new_component)
        self.log.debug(
            'Extracted {0!r} from {1!r}'.format(
                new_component, instance.name
            )
        )


pyblish.api.register_plugin(ExtractNukeScriptComponent)
