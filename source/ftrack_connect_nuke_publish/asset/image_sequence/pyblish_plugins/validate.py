# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import pyblish.api


class ImageSequencePublishValidator(pyblish.api.InstancePlugin):
    '''Validate Geo publish.'''

    order = pyblish.api.ValidatorOrder

    families = ['ftrack', 'write']
    match = pyblish.api.Subset

    label = 'Validate Image Sequence component.'
    optional = False

    def check_frames(self, input_frames, write_node, instance_name):
        '''Check that all the frames expressed in *input_frames* exists.
        It'll use *write_node* and *instance_name* to fetch data and report.
        '''

        import nuke
        import os
        import clique
        import glob

        self.log.info(
            'Validating {0} from {1}'.format(input_frames, instance_name)
        )

        single_file = os.path.isfile(input_frames)
        if not single_file:

            first = str(int(nuke.root().knob('first_frame').value()))
            last = str(int(nuke.root().knob('last_frame').value()))

            # Then in case check if the limit are set.
            if write_node['use_limit'].value():
                first = str(write_node['first'].value())
                last = str(write_node['last'].value())

            # Always check how many frames are actually available.
            frames = input_frames

            try:
                # Try to collect the sequence prefix, padding
                # and extension. If this fails with a ValueError
                # we are probably handling a non-sequence file.
                # If so rely on the first_frame and last_frame
                # of the root node.
                prefix, padding, extension = frames.split('.')
            except ValueError:
                msg = (
                    'Could not determine prefix, padding '
                    'and extension from "{0}".'.format(frames)
                )
                self.log.error(msg)
                assert False, msg

            else:
                root = os.path.dirname(prefix)
                file_name = os.path.basename(prefix)
                frame_query = '{0}/{1}*.{2}'.format(
                    root, file_name, extension
                )
                self.log.debug('Looking for {0}'.format(frame_query))

                files = glob.glob(frame_query)
                collections = clique.assemble(files)
                frame_collection = collections[0]
                if len(frame_collection) > 0:
                    frames = frame_collection[0]
                else:
                    assert False, 'frames : {0} has not been not found'.format(
                        frames
                    )

                for frame in frames:
                    name, number, ext = frame.split('.')
                    # check only frames in the current range
                    frame_path = os.path.join(root, frame)
                    in_range = int(first) <= int(number) <= int(last)

                    if in_range:
                        assert os.path.exists(
                            frame_path
                        ), 'Frame {0} does not exist!'.format(
                            frame_path
                        )
                    else:
                        self.log.warning(
                            'Not Checking frame {0} '
                            'as is out of the current range. {1}-{2}'.format(
                                frame_path, first, last
                            )
                        )

        else:
            assert os.path.exists(
                input_frames
            ), 'File {0} does not exist!'.format(input_frames)

    def process(self, instance):
        '''Validate *instance*.'''
        import nuke

        write_node = nuke.toNode(instance.name)
        file_comp = str(write_node['file'].value())
        proxy_comp = str(write_node['proxy'].value())
        for comp_data in [file_comp, proxy_comp]:
            if comp_data:
                self.check_frames(comp_data, write_node, instance.name)
