# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import pyblish.api
import nuke
import tempfile

class ExtractCameraNukeChan(pyblish.api.InstancePlugin):
    '''prepare component to be published'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack.nuke.camera']

    def process(self, instance):
        '''Process *instance* and extract media.'''
        '''
        # generate temp file
        temporary_path = tempfile.mkstemp(suffix='.mb')[-1]

        # save chan file
        # ...

        name = instance.name
        if name.startswith('|'):
            name = name[1:]

        new_component = {
            'name': '%s.mayabinary' % name,
            'path': temporary_path,
        }

        print 'Adding new component: %s' % new_component
        instance.data['ftrack_components'].append(new_component)
        '''
        pass

pyblish.api.register_plugin(ExtractCameraNukeChan)
