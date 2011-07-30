# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'TwitterUser.candidate'
        db.alter_column('tweets_twitteruser', 'candidate_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Campaign']))

        # Changing field 'Tweet.text'
        db.alter_column('tweets_tweet', 'text', self.gf('django.db.models.fields.CharField')(max_length=200))
    
    
    def backwards(self, orm):
        
        # Changing field 'TwitterUser.candidate'
        db.alter_column('tweets_twitteruser', 'candidate_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Candidate']))

        # Changing field 'Tweet.text'
        db.alter_column('tweets_tweet', 'text', self.gf('django.db.models.fields.CharField')(max_length=140))
    
    
    models = {
        'base.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'})
        },
        'tweets.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'twitter_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tweets.TwitterUser']"})
        },
        'tweets.twitteruser': {
            'Meta': {'object_name': 'TwitterUser'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Campaign']"}),
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
