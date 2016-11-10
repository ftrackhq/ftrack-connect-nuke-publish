# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api
import clique
import os
import glob


class ExtractWriteNodes(pyblish.api.InstancePlugin):
    '''Extract nuke media from write nodes.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack.nuke.write']

    def process(self, instance):
        '''Process *instance* and extract media.'''

        self.log.debug(
            'Started extracting write node {0!r}'.format(
                instance.name
            )
        )

        import nuke
        write_node = nuke.toNode(instance.name)
        file_comp = str(write_node['file'].value())
        proxy_comp = str(write_node['proxy'].value())
        name_comp = str(write_node['name'].value()).strip()

        # use the timeline to define the amount of frames
        first = str(int(nuke.root().knob('first_frame').value()))
        last = str(int(nuke.root().knob('last_frame').value()))

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
                'and extension from "{0}".'.format(frames)
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

        if first != last:
            sequence_path = u'{0} [{1}-{2}]'.format(
                file_comp, first, last
            )
        else:
            sequence_path = unicode(file_comp % first)

        new_component = {
            'path': sequence_path,
            'name': name_comp,
            'first': first,
            'last': last,
            'node_name': name_comp
        }

        instance.data['ftrack_components'].append(new_component)
        self.log.debug(
            'Extracted {0!r} from {1!r}'.format(
                new_component, instance.name
            )
        )

        if proxy_comp != '':

            if first != last:
                sequence_path = u'{0} [{1}-{2}]'.format(
                    proxy_comp, first, last
                )
            else:
                sequence_path = unicode(proxy_comp % first)

            new_component = {
                'file_path': new_component,
                'name': name_comp + '_proxy',
                'first': first,
                'last': last,
                'node_name': name_comp
            }

            instance.data['ftrack_components'].append(new_component)

            self.log.debug(
                'Extracted {0!r} from {1!r}'.format(
                    new_component, instance.name
                )
            )
