from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


class BodyField(StreamField):
    def __init__(self, block_types=None, **kwargs):
        block_types = [
            ('Heading', blocks.CharBlock(icon="title", classname="heading")),
            ('Paragraph', ParagraphBlock()),
            ('Image', ImageChooserBlock(icon="image")),
            ('Embed', EmbedBlock(icon="site")),
            ('List', blocks.ListBlock(blocks.RichTextBlock(label="item"), icon="list-ul")),
            ('Sharable', SharableBlock()),
            ('AuthorBlurb', AuthorBlurbBlock()),
        ]

        super(BodyField, self).__init__(block_types, **kwargs)


class SharableBlock(blocks.CharBlock):
    class Meta:
        template = "articles/blocks/sharable.html"
        icon = "openquote"


class AuthorBlurbBlock(blocks.CharBlock):
    class Meta:
        template = "articles/blocks/author_blurb.html"
        icon = "user"


class ParagraphBlock(blocks.StructBlock):
    use_dropcap = blocks.BooleanBlock(required=False)
    text = blocks.RichTextBlock()

    class Meta:
        template = "articles/blocks/paragraph_block.html"
        icon = "doc-full"
