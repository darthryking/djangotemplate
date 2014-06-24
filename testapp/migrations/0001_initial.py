# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestObject'
        db.create_table(u'testapp_testobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('intField', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('charField', self.gf('django.db.models.fields.CharField')(default='a', max_length=1)),
            ('textField', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'testapp', ['TestObject'])


    def backwards(self, orm):
        # Deleting model 'TestObject'
        db.delete_table(u'testapp_testobject')


    models = {
        u'testapp.testobject': {
            'Meta': {'object_name': 'TestObject'},
            'charField': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intField': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'textField': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['testapp']