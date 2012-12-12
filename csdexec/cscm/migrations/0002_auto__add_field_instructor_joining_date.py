# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Instructor.joining_date'
        db.add_column('cscm_instructor', 'joining_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 12, 12, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Instructor.joining_date'
        db.delete_column('cscm_instructor', 'joining_date')


    models = {
        'cscm.course': {
            'Meta': {'object_name': 'Course'},
            'batch': ('django.db.models.fields.CharField', [], {'default': "'BS11'", 'max_length': '10'}),
            'class_time_spent': ('django.db.models.fields.CharField', [], {'default': "',,,'", 'max_length': '50'}),
            'course_code': ('django.db.models.fields.CharField', [], {'default': "'CS'", 'max_length': '10'}),
            'course_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'course_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'course_url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'credits': ('django.db.models.fields.IntegerField', [], {}),
            'grade_distribution': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'lab_projects': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oral_written_details': ('django.db.models.fields.CharField', [], {'default': "',,,'", 'max_length': '20'}),
            'pre_reqs': ('django.db.models.fields.TextField', [], {}),
            'prog_assignments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'cscm.courselogentry': {
            'Meta': {'object_name': 'CourseLogEntry'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Course']"}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'evaluation_instruments': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture_date': ('django.db.models.fields.DateField', [], {}),
            'lecture_no': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'topics_covered': ('django.db.models.fields.TextField', [], {}),
            'week_no': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'cscm.courseoutline': {
            'Meta': {'object_name': 'CourseOutline'},
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cscm.Course']", 'unique': 'True'}),
            'course_policies': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objectives': ('django.db.models.fields.TextField', [], {}),
            'other_information': ('django.db.models.fields.TextField', [], {}),
            'recommended_books': ('django.db.models.fields.TextField', [], {}),
            'text_books': ('django.db.models.fields.TextField', [], {})
        },
        'cscm.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'age': ('django.db.models.fields.CharField', [], {'default': '25', 'max_length': '200'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joining_date': ('django.db.models.fields.DateField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'cscm.weekplan': {
            'Meta': {'object_name': 'WeekPlan'},
            'course_outline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.CourseOutline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topics': ('django.db.models.fields.TextField', [], {'default': "'Please insert topics here'"}),
            'week_no': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['cscm']