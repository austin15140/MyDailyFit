# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Signup.id'
        db.alter_column(u'home_signup', 'id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True))

    def backwards(self, orm):

        # Changing field 'Signup.id'
        db.alter_column(u'home_signup', u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

    models = {
        u'home.signup': {
            'Meta': {'object_name': 'Signup'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['home']