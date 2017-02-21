# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api


class ReviewableComponentExtract(pyblish.api.InstancePlugin):
    '''Create temporary Scene and WriteGeo nodes and initialize them.'''

    order = pyblish.api.ExtractorOrder - 0.1

    families = ['ftrack']
    match = pyblish.api.Subset

    def process(self, instance):

        from ftrack_connect_pipeline import constant

        make_reviewable = instance.context.data['options'].get(
            constant.REVIEWABLE_COMPONENT_OPTION_NAME, False
        )

        has_reviewable = instance.context.data['options'].get(
            'ftrack_reviewable_component'
        )

        if not make_reviewable or has_reviewable:
            return

        '''Process *instance*.'''
        self.log.debug(
            'Pre extracting reviewable component {0!r}'.format(
                instance.name
            )
        )

        import tempfile
        import nuke
        write = nuke.toNode(instance.name)

        # Get the input of the given write node.
        input_node = write.input(0)

        # Generate output file name for mov.
        temp_review_mov = tempfile.NamedTemporaryFile(suffix='.mov').name

        first = str(int(nuke.root().knob('first_frame').value()))
        last = str(int(nuke.root().knob('last_frame').value()))

        # Create a new write_node.
        review_node = nuke.createNode('Write')
        review_node.setInput(0, input_node)
        review_node['file'].setValue(temp_review_mov)
        review_node['file_type'].setValue('mov')
        review_node['mov64_codec'].setValue('png')

        ranges = nuke.FrameRanges('{0}-{1}'.format(first, last))
        nuke.render(review_node, ranges)

        instance.data['ftrack_tmp_review_node'] = review_node['name'].value()
        instance.context.data['options'].setdefault(
            'ftrack_reviewable_component', temp_review_mov
        )

        self.log.debug(
            'Extracted Reviewable component from {0!r}'.format(
                instance.name
            )
        )


class PostReviewableComponentExtract(pyblish.api.InstancePlugin):
    '''Remove temporary Scene and WriteGeo nodes.'''

    order = pyblish.api.ExtractorOrder + 0.1

    families = ['ftrack']
    match = pyblish.api.Subset

    def process(self, instance):
        '''Process *instance*.'''
        from ftrack_connect_pipeline import constant

        make_reviewable = instance.context.data['options'].get(
            constant.REVIEWABLE_COMPONENT_OPTION_NAME, False
        )

        if make_reviewable and instance.data.get('ftrack_tmp_review_node'):
            self.log.debug(
                'Post extracting reviewable component {0!r}'.format(
                    instance.name
                )
            )

            import nuke
            node_name = instance.data['ftrack_tmp_review_node']
            nuke.delete(nuke.toNode(node_name))


pyblish.api.register_plugin(ReviewableComponentExtract)
pyblish.api.register_plugin(PostReviewableComponentExtract)
