# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InstructorPublication.author_list'
        db.add_column('csip_instructorpublication', 'author_list',
                      self.gf('django.db.models.fields.TextField')(default='Author name'),
                      keep_default=False)

        # Adding field 'InstructorPublication.title'
        db.add_column('csip_instructorpublication', 'title',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InstructorPublication.journal'
        db.add_column('csip_instructorpublication', 'journal',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InstructorPublication.volume'
        db.add_column('csip_instructorpublication', 'volume',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InstructorPublication.number'
        db.add_column('csip_instructorpublication', 'number',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InstructorPublication.publisher'
        db.add_column('csip_instructorpublication', 'publisher',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InstructorPublication.pub_date'
        db.add_column('csip_instructorpublication', 'pub_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 12, 18, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'InstructorPublication.hec_cat'
        db.add_column('csip_instructorpublication', 'hec_cat',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'InstructorPublication.author_list'
        db.delete_column('csip_instructorpublication', 'author_list')

        # Deleting field 'InstructorPublication.title'
        db.delete_column('csip_instructorpublication', 'title')

        # Deleting field 'InstructorPublication.journal'
        db.delete_column('csip_instructorpublication', 'journal')

        # Deleting field 'InstructorPublication.volume'
        db.delete_column('csip_instructorpublication', 'volume')

        # Deleting field 'InstructorPublication.number'
        db.delete_column('csip_instructorpublication', 'number')

        # Deleting field 'InstructorPublication.publisher'
        db.delete_column('csip_instructorpublication', 'publisher')

        # Deleting field 'InstructorPublication.pub_date'
        db.delete_column('csip_instructorpublication', 'pub_date')

        # Deleting field 'InstructorPublication.hec_cat'
        db.delete_column('csip_instructorpublication', 'hec_cat')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cscm.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'age': ('django.db.models.fields.CharField', [], {'default': '25', 'max_length': '200'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joining_date': ('django.db.models.fields.DateField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'csip.instructorconsultancy': {
            'Meta': {'object_name': 'InstructorConsultancy'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'csip.instructoreducation': {
            'Meta': {'object_name': 'InstructorEducation'},
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'csip.instructoremployment': {
            'Meta': {'object_name': 'InstructorEmployment'},
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'job_desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'csip.instructoreventparticpation': {
            'Meta': {'object_name': 'InstructorEventParticpation'},
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'role': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'venue': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'csip.instructorprofile': {
            'Meta': {'object_name': 'InstructorProfile'},
            'admin_responsibility': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'awards': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'current_position_appointment_date': ('django.db.models.fields.DateField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gross_pay': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cscm.Instructor']", 'unique': 'True'}),
            'joining_date': ('django.db.models.fields.DateField', [], {}),
            'memberships': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pay_grade': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pay_step': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'csip.instructorpublication': {
            'Meta': {'object_name': 'InstructorPublication'},
            'author_list': ('django.db.models.fields.TextField', [], {}),
            'hec_cat': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impact_factor': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'journal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pub_bib': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'pub_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'publisher': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'volume': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['csip']