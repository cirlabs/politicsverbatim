# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Source'
        db.create_table('base_source', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('base', ['Source'])

        # Adding model 'DocumentType'
        db.create_table('base_documenttype', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('base', ['DocumentType'])

        # Adding model 'ExcerptType'
        db.create_table('base_excerpttype', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('base', ['ExcerptType'])

        # Adding model 'Campaign'
        db.create_table('base_campaign', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True, db_index=True)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('base', ['Campaign'])

        # Adding model 'Location'
        db.create_table('base_location', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('lat', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('lng', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('base', ['Location'])

        # Adding model 'Category'
        db.create_table('base_category', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('base', ['Category'])

        # Adding model 'Document'
        db.create_table('base_document', (
            ('date_entered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('quality', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Source'])),
            ('source_date', self.gf('django.db.models.fields.DateField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DocumentType'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True, db_index=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Location'], null=True, blank=True)),
        ))
        db.send_create_signal('base', ['Document'])

        # Adding model 'Excerpt'
        db.create_table('base_excerpt', (
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Document'])),
            ('date_entered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Campaign'])),
        ))
        db.send_create_signal('base', ['Excerpt'])

        # Adding M2M table for field category on 'Excerpt'
        db.create_table('base_excerpt_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('excerpt', models.ForeignKey(orm['base.excerpt'], null=False)),
            ('category', models.ForeignKey(orm['base.category'], null=False))
        ))
        db.create_unique('base_excerpt_category', ['excerpt_id', 'category_id'])

        # Adding M2M table for field type on 'Excerpt'
        db.create_table('base_excerpt_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('excerpt', models.ForeignKey(orm['base.excerpt'], null=False)),
            ('excerpttype', models.ForeignKey(orm['base.excerpttype'], null=False))
        ))
        db.create_unique('base_excerpt_type', ['excerpt_id', 'excerpttype_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Source'
        db.delete_table('base_source')

        # Deleting model 'DocumentType'
        db.delete_table('base_documenttype')

        # Deleting model 'ExcerptType'
        db.delete_table('base_excerpttype')

        # Deleting model 'Campaign'
        db.delete_table('base_campaign')

        # Deleting model 'Location'
        db.delete_table('base_location')

        # Deleting model 'Category'
        db.delete_table('base_category')

        # Deleting model 'Document'
        db.delete_table('base_document')

        # Deleting model 'Excerpt'
        db.delete_table('base_excerpt')

        # Removing M2M table for field category on 'Excerpt'
        db.delete_table('base_excerpt_category')

        # Removing M2M table for field type on 'Excerpt'
        db.delete_table('base_excerpt_type')
    
    
    models = {
        'base.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'})
        },
        'base.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'})
        },
        'base.document': {
            'Meta': {'object_name': 'Document'},
            'date_entered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Source']"}),
            'source_date': ('django.db.models.fields.DateField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DocumentType']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'base.documenttype': {
            'Meta': {'object_name': 'DocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'})
        },
        'base.excerpt': {
            'Meta': {'object_name': 'Excerpt'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Campaign']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.Category']", 'blank': 'True'}),
            'date_entered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.ExcerptType']", 'null': 'True', 'blank': 'True'})
        },
        'base.excerpttype': {
            'Meta': {'object_name': 'ExcerptType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'})
        },
        'base.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'lng': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'base.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }
    
    complete_apps = ['base']
