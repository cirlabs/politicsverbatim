# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'TwitterUser'
        db.create_table('tweets_twitteruser', (
            ('statuses_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Candidate'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('friends_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('profile_image_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('followers_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('tweets', ['TwitterUser'])

        # Adding model 'Tweet'
        db.create_table('tweets_tweet', (
            ('tweet_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweets.TwitterUser'])),
        ))
        db.send_create_signal('tweets', ['Tweet'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'TwitterUser'
        db.delete_table('tweets_twitteruser')

        # Deleting model 'Tweet'
        db.delete_table('tweets_tweet')
    
    
    models = {
        'base.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'})
        },
        'tweets.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'twitter_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tweets.TwitterUser']"})
        },
        'tweets.twitteruser': {
            'Meta': {'object_name': 'TwitterUser'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Candidate']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'followers_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'friends_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'profile_image_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'statuses_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }
    
    complete_apps = ['tweets']
