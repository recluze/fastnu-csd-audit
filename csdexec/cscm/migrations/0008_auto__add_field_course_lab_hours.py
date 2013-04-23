# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.lab_hours'
        db.add_column('cscm_course', 'lab_hours',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Course.lab_hours'
        db.delete_column('cscm_course', 'lab_hours')


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
        'cscm.course': {
            'Meta': {'object_name': 'Course'},
            'batch': ('django.db.models.fields.CharField', [], {'default': "'BS11'", 'max_length': '10'}),
            'class_time_spent_analysis': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'class_time_spent_design': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'class_time_spent_ethics': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'class_time_spent_theory': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'communciation_details_num_mins': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'communciation_details_num_pres': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'communciation_details_num_reports': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'communciation_details_pages': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'course_code': ('django.db.models.fields.CharField', [], {'default': "'CS'", 'max_length': '10'}),
            'course_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'course_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'course_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'credits': ('django.db.models.fields.IntegerField', [], {}),
            'grade_distribution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'lab_hours': ('django.db.models.fields.IntegerField', [], {}),
            'lab_projects': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pre_reqs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'prog_assignments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'cscm.courselogentry': {
            'Meta': {'object_name': 'CourseLogEntry'},
            'contents_covered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Course']"}),
            'duration': ('django.db.models.fields.CharField', [], {'default': '1.5', 'max_length': '5'}),
            'evaluation_instruments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture_date': ('django.db.models.fields.DateField', [], {}),
            'other_activities': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reading_materials': ('django.db.models.fields.TextField', [], {'default': "'Lecture Slides'", 'blank': 'True'}),
            'topics_covered': ('django.db.models.fields.TextField', [], {})
        },
        'cscm.courseoutline': {
            'Meta': {'object_name': 'CourseOutline'},
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cscm.Course']", 'unique': 'True'}),
            'course_policies': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objectives': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'other_information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'outcomes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recommended_books': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_books': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'cscm.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'age': ('django.db.models.fields.CharField', [], {'default': '25', 'max_length': '200'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joining_date': ('django.db.models.fields.DateField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cscm.weekplan': {
            'Meta': {'object_name': 'WeekPlan'},
            'course_outline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.CourseOutline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topics': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'week_no': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['cscm']