from django import template

register = template.Library()
# {% video self.intro_video extra_att extra_att poster=some_wagtail_image %}


@register.tag(name="video")
def video(parser, token):
    template_params = token.split_contents()[1:]  # Everything after 'video'
    video_expr = template_params[0]

    extra_attrs = {}

    # Everyting after video expression
    if(len(template_params) > 1):
        for param in template_params[1:]:
            try:
                name, value = param.split('=')
                extra_attrs[name] = value
            except ValueError:
                extra_attrs[param] = ''  # attributes without values e.g. autoplay, controls
    return VideoNode(video_expr, extra_attrs)


class VideoNode(template.Node):
    def __init__(self, video, attrs={}):
        self.video = template.Variable(video)
        self.attrs = attrs
        try:
            self.poster = template.Variable(attrs['poster'])
        except KeyError:
            self.poster = None

    def render(self, context):
        video = self.video.resolve(context)

        if not video:
            raise template.TemplateSyntaxError("video tag requires a Video object as the first parameter")

        if self.poster:
            poster = self.poster.resolve(context)
        else:
            poster=False

        return video.video_tag(poster, self.attrs)
