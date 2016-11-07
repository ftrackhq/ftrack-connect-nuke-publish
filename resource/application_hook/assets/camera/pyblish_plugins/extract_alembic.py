# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import pyblish.api
import nuke
import tempfile


class PreCameraAlembicExtract(pyblish.api.InstancePlugin):
    '''Create temporary Scene and WriteGeo nodes and initialize them.'''

    order = pyblish.api.ExtractorOrder - 0.1

    families = ['ftrack.nuke.camera']

    def process(self, instance):
        camera_node = nuke.toNode(instance.name)

        scn = nuke.nodes.Scene()
        scn.setInput(0, camera_node)
        instance.data['nuke_scene'] = scn

        wrt = nuke.nodes.WriteGeo()
        wrt.setInput(0, scn)
        wrt['file_type'].setValue('abc')
        wrt['writeCameras'].setValue(True)
        wrt['writeGeometries'].setValue(False)
        wrt['writeAxes'].setValue(False)
        wrt['writePointClouds'].setValue(False)
        wrt['storageFormat'].setValue("Ogawa") # or HDF5?
        instance.data['nuke_write'] = wrt


class ExtractCameraAlembic(pyblish.api.InstancePlugin):
    '''Prepare component to be published.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack.nuke.camera']

    def process(self, instance):
        '''Process *instance*.'''

        write_node = instance.data['nuke_write']
        temporary_path = tempfile.mkstemp(suffix='.abc')[-1]
        write_node['file'].setValue(temporary_path)

        nuke.execute(write_node.name())
        new_component = {
            'name': '%s.alembic' % instance.name,
            'path': temporary_path,
        }

        print 'Adding new component: %s' % new_component
        instance.data['ftrack_components'].append(new_component)


class PostCameraAlembicExtract(pyblish.api.InstancePlugin):
    '''Remove temporary Scene and WriteGeo nodes.'''

    order = pyblish.api.ExtractorOrder + 0.1

    families = ['ftrack.nuke.camera']

    def process(self, instance):
        nuke.delete(instance.data['nuke_write'])
        nuke.delete(instance.data['nuke_scene'])


pyblish.api.register_plugin(PreCameraAlembicExtract)
pyblish.api.register_plugin(ExtractCameraAlembic)
pyblish.api.register_plugin(PostCameraAlembicExtract)