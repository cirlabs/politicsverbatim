import datetime
from django import template
from blog.models import Post

register = template.Library()

@register.tag
def truncatewords_html_readmore(parser, token):
    bits = token.contents.split()
    if len(bits) < 4:
        raise template.TemplateSyntaxError(u'%s requires 4 arguments')

    return TruncateNode(bits[1], bits[2], bits[3])

class TruncateNode(template.Node):
    def __init__(self, value, length, post):
        self.value = template.Variable(value)
        self.length = int(length)
        self.post = template.Variable(post)

    def render(self, context):
        from django.utils.text import truncate_html_words
        value = self.value.resolve(context)
        post = self.post.resolve(context)
        end_text = '... <a href="%s">Read more</a>' % post.get_absolute_url()
        return truncate_html_words(value, self.length, end_text)


@register.tag
def posts_per_month(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(u'%s requires a date object')

    return PostsPerMonthNode(bits[1])

class PostsPerMonthNode(template.Node):
    def __init__(self, date):
        self.date = template.Variable(date)

    def render(self, context):
        date = self.date.resolve(context)
        return Post.objects.filter(publication_date__year=date.year, publication_date__month=date.month).count()
