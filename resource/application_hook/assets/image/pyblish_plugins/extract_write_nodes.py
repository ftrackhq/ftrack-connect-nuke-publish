import pyblish.api


class ExtractWriteNodes(pyblish.api.InstancePlugin):
    '''Extract nuke media from write nodes.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack.nuke.write']

    def process(self, instance):
        '''Process *instance* and extract media.'''

        print "*** Extracting paths from write nodes!!!"

        if instance.data.get('publish'):
            print (
                'Extracting media using options:',
                instance.data.get('options')
            )
            instance.data['ftrack_components'].append(
                {
                    'name': instance.name,
                    'path': instance.data.get('options')['path'],
                }
            )

pyblish.api.register_plugin(ExtractWriteNodes)
