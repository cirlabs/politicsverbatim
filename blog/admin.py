from django.contrib import admin
from django.conf import settings
from blog.models import Post
from utils.tinymce.widgets import TinyMCE

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('headline',)}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20}, )},
    }
    fieldsets = (
        ('The basics', {
            'fields': ('author', 'headline', ('publication_date', 'publication_status'), 'body', 'image'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('slug',)
        }),
    )
    search_fields = ['headline', 'body']
    list_filter = ['publication_status']
    list_display = ('headline', 'publication_date', 'publication_status', 'created_date', 'updated_date')

    class Media:
        js = [settings.MEDIA_URL + 'js/tinymce/jscripts/tiny_mce/tiny_mce.js']
admin.site.register(Post, PostAdmin)