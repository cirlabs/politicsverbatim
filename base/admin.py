from django.contrib import admin
from base.models import *
from tinymce.widgets import TinyMCE

########## INLINES ##########

class ExcerptInline(admin.TabularInline):
    model = Excerpt
    verbose_name = 'Excerpts'
    verbose_name_plural = 'Excerpts'
    extra = 3

########## ADMINS ##########

class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ExcerptInline]
    fieldsets = (
        ('The basics', {
            'fields': ('name', ('type', 'source'), ('source_date', 'status'))
        }),
        ('Location information', {
            'fields': ('location',)
        }),   
        ('Document details', {
            'fields': ('url', 'file', 'text')
        }),      
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('slug',)
        }),
    )
    search_fields = ['name', 'text']
    list_filter = ['source', 'type']
    list_display = ('__unicode__', 'source', 'type', 'source_date', 'date_entered')
admin.site.register(Document, DocumentAdmin)

class ExcerptAdmin(admin.ModelAdmin):
    pass
admin.site.register(Excerpt, ExcerptAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class SourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Source, SourceAdmin)

class DocumentTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(DocumentType, DocumentTypeAdmin)

class ExcerptTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(ExcerptType, ExcerptTypeAdmin)
 
class CampaignAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20}, )},
    }
admin.site.register(Campaign, CampaignAdmin)

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('city', 'state')}
admin.site.register(Location, LocationAdmin)

class CampaignTopicAdmin(admin.ModelAdmin):
    filter_horizontal = ('supporting_excerpts',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20}, )},
    }
admin.site.register(CampaignTopic, CampaignTopicAdmin)

########## UNUSED ADMINS FOR RDF EXPERIMENT ##########

#class ExcerptRelationAdmin(admin.ModelAdmin):
#    prepopulated_fields = {'slug': ('relation_name',)}
#admin.site.register(ExcerptRelation, ExcerptRelationAdmin)

#class ExcerptMappingAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(ExcerptMapping, ExcerptMappingAdmin)
