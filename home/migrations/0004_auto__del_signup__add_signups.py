# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Signup'
        db.delete_table(u'home_signup')

        # Adding model 'Signups'
        db.create_table(u'home_signups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal(u'home', ['Signups'])


    def backwards(self, orm):
        # Adding model 'Signup'
        db.create_table(u'home_signup', (
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'home', ['Signup'])

        # Deleting model 'Signups'
        db.delete_table(u'home_signups')


    models = {
        u'home.signups': {
            'Meta': {'object_name': 'Signups'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['home']