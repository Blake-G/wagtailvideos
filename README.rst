wagtailvideos
=============

Based on wagtailimages. The aim was to have feature parity with images
but for html5 videos. Includes the ability to transcode videos to a
html5 compliant codec using ffmpeg.

Requirements
------------

-  Wagtail >= 2.4
-  `ffmpeg <https://ffmpeg.org/>`__

Installing
----------

Install using pypi

.. code:: bash

    pip install wagtailvideos (the original package)
    or
    pip install git+https://github.com/emg36/wagtailvideos.git (this package fork)


Using
-----

On a page model:
~~~~~~~~~~~~~~~~

Implement as a ``ForeignKey`` relation, same as wagtailimages.

.. code:: python


    from django.db import models

    from wagtail.wagtailadmin.edit_handlers import FieldPanel
    from wagtail.wagtailcore.fields import RichTextField
    from wagtail.wagtailcore.models import Page

    from wagtailvideos.edit_handlers import VideoChooserPanel

    class HomePage(Page):
        body = RichtextField()
        header_video = models.ForeignKey(
            'wagtailvideos.Video',
            related_name='+',
            null=True,
            on_delete=models.SET_NULL,
            )

        content_panels = Page.content_panels + [
            FieldPanel('body'),
            VideoChooserPanel('header_video'),
        ]

In template:
~~~~~~~~~~~~

The video template tag takes one required postitional argument, a video
field. All extra attributes are added to the surrounding ``<video>``
tag. The original video and all extra transcodes are added as
``<source>`` tags.

.. code:: django

    {% load wagtailvideos_tags %}
    {% video self.header_video autoplay controls width=256 %}

You can specify a poster using a url like e.g. from google or reference your own image.url. 
This is how I'm currently getting around not being able to use a wagtail image as the thumbnail image
due to the video and image chooser inception problems. The thumbnail image is still a part of the model
because you might want to use it as is and it's still useful for knowing what the video is.

So my model might look something like 

.. code:: python
    class HomePage(Page):
        body = RichtextField()
        header_video_poster = models.ForeignKey(
            'wagtailimages.Image',
            related_name='+',
            blank=True,
            null=True,
            on_delete=models.SET_NULL
            
        header_video = models.ForeignKey(
            'wagtailvideos.Video',
            related_name='+',
            blank=True,
            null=True,
            on_delete=models.SET_NULL
            )
        content_panels = Page.content_panels + [
            FieldPanel('body'),
            ImageChooserPanel(header_video_poster),
            VideoChooserPanel('header_video'),
        ]
.. code:: django
    {% load wagtailvideos_tags wagtailimages_tags %}
    {% image header_video_poster.image fill-400x400 as img %}
    {% video self.header_video autoplay controls width=256 poster=img.url %}
    or 
    {% video self.header_video autoplay controls width=256 poster='http://example.com/some-image.jpg' %}


How to transcode using ffmpeg:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using the video collection manager from the left hand menu. In the video
editing section you can see the available transcodes and a form that can
be used to create new transcodes. It is assumed that your compiled
version of ffmpeg has the matching codec libraries required for the
transcode.

Future features
---------------

-  Richtext embed
-  Streamfield block
-  Transcoding via amazon service rather than ffmpeg
-  Wagtail homescreen video count
