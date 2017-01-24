# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import pyblish.api


class ExtractWriteGeoNodes(pyblish.api.InstancePlugin):
    '''Extract nuke geo from write geo nodes.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'geo']
    match = pyblish.api.Subset

    def process(self, instance):
        '''Process *instance* and extract geo.'''

        self.log.debug(
            'Started extracting write geo node {0!r}'.format(
                instance.name
            )
        )

        import nuke

        writegeo_node = nuke.toNode(instance.name)
        file_comp = str(writegeo_node['file'].value())
        node_name = str(writegeo_node['name'].value()).strip()
        component_name = "alembic"
        self.log.debug('Using component name: {0!r}'.format(component_name))

        new_component = {
            'path': file_comp,
            'name': component_name,
            'node_name': node_name
        }
        instance.data['ftrack_components'].append(new_component)

        self.log.debug(
            'Extracted {0!r} from {1!r}'.format(
                new_component, instance.name
            )
        )
