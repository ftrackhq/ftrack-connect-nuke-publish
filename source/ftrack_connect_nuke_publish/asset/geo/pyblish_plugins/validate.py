# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import pyblish.api


class GeoPublishValidator(pyblish.api.InstancePlugin):
    '''Validate Geo publish.'''

    order = pyblish.api.ValidatorOrder

    families = ['ftrack', 'geo']
    match = pyblish.api.Subset

    label = 'Validate Alembic component.'
    optional = False

    def process(self, instance):
        import nuke

        node = nuke.toNode(instance.name)
        file_comp = str(node['file'].value())

        self.log.debug(
            'Validating {0} from {1}'.format(
                file_comp, instance.name
            )
        )

        import os
        filename, extension = os.path.splitext(file_comp)

        # extension is not '.abc' does not work. Maybe a python bug?
        if extension.lower() != '.abc':
            error_msg = 'Geometry file for node {0} is not an alembic file'.format(
                instance.name
                )
            assert False, error_msg

        if not os.path.exists(file_comp):
            error_msg = 'Alembic file for node {0} does not exist.'.format(
                instance.name
                )
            assert False, error_msg
