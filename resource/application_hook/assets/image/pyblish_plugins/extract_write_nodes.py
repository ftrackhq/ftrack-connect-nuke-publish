
import pyblish.api

import nuke

import clique

import os
import glob


class ExtractWriteNodes(pyblish.api.InstancePlugin):
    '''Extract nuke media from write nodes.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack.nuke.write']

    def process(self, instance):
        '''Process *instance* and extract media.'''

        media_options = instance.context.data['options'].get(
            'nuke_media_options', {}
        )

        write_node = nuke.toNode(instance.name)
        file_comp = str(write_node['file'].value())
        proxy_comp = str(write_node['proxy'].value())
        name_comp = str(write_node['name'].value()).strip()

        # use the timeline to define the amount of frames
        first = str(int(nuke.root().knob("first_frame").value()))
        last = str(int(nuke.root().knob("last_frame").value()))

        # then in case check if the limit are set
        if write_node['use_limit'].value():
            first = str(write_node['first'].value())
            last = str(write_node['last'].value())

        # always check how many frames are actually available
        frames = write_node['file'].value()

        try:
            # Try to collect the sequence prefix, padding
            # and extension. If this fails with a ValueError
            # we are probably handling a non-sequence file.
            # If so rely on the first_frame and last_frame
            # of the root node.
            prefix, padding, extension = frames.split('.')
        except ValueError:
            print(
                'Could not determine prefix, padding '
                'and extension from "".'.format(frames)
            )
        else:
            root = os.path.dirname(prefix)
            files = glob.glob('{0}/*.{1}'.format(root, extension))
            collections = clique.assemble(files)

            for collection in collections[0]:
                if prefix in collection.head:
                    indexes = list(collection.indexes)
                    first = str(indexes[0])
                    last = str(indexes[-1])
                    break

        try:
            comp_name_comp = write_node['fcompname'].value()
        except:
            comp_name_comp = ''

        if comp_name_comp == '':
            comp_name_comp = name_comp

        new_component = {
            'file_path'         : file_comp,
            'component_name'    : comp_name_comp + "_" + name_comp,
            'first'             : first,
            'last'              : last,
            'node_name'         : name_comp
        }

        instance.data['ftrack_components'].append(new_component)

        if proxy_comp != '':
            new_component = {
                'file_path'         : proxy_comp,
                'component_name'    : comp_name_comp + "_" + name_comp + "_proxy",
                'first'             : first,
                'last'              : last,
                'node_name'         : name_comp
            }

            instance.data['ftrack_components'].append(new_component)

        # todo: Handle copy files if enabled...
        # todo: Attach nukescript if enabled...

pyblish.api.register_plugin(ExtractWriteNodes)

# Silence ftrack warnings about missing register functions.
def register(session):
    pass
