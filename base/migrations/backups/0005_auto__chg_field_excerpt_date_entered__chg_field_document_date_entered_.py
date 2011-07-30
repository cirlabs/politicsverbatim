# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Excerpt.date_entered'
        db.alter_column('base_excerpt', 'date_entered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))

        # Changing field 'Document.date_entered'
        db.alter_column('base_document', 'date_entered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))

        # Changing field 'Document.url'
        db.alter_column('base_document', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, unique=True, null=True, blank=True))

        # Adding unique constraint on 'Document', fields ['url']
        db.create_unique('base_document', ['url'])


    def backwards(self, orm):
        
        # Changing field 'Excerpt.date_entered'
        db.alter_column('base_excerpt', 'date_entered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))

        # Changing field 'Document.date_entered'
        db.alter_column('base_document', 'date_entered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))

        # Changing field 'Document.url'
        db.alter_column('base_document', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True))

        # Removing unique constraint on 'Document', fields ['url']
        db.delete_unique('base_document', ['url'])


    models = {
        'base.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'base.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'base.document': {
            'Meta': {'object_name': 'Document'},
            'date_entered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Source']"}),
            'source_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DocumentType']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'base.documenttype': {
            'Meta': {'object_name': 'DocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'base.excerpt': {
            'Meta': {'object_name': 'Excerpt'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Campaign']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'date_entered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['base.ExcerptType']", 'null': 'True', 'blank': 'True'})
        },
        'base.excerptmapping': {
            'Meta': {'object_name': 'ExcerptMapping'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_excerpts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'object_excerpt'", 'symmetrical': 'False', 'to': "orm['base.Excerpt']"}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.ExcerptRelation']"}),
            'subject_excerpt': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subject_excerpt'", 'to': "orm['base.Excerpt']"})
        },
        'base.excerptrelation': {
            'Meta': {'object_name': 'ExcerptRelation'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relation_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'base.excerpttype': {
            'Meta': {'object_name': 'ExcerptType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'base.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'lng': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'base.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['base']
