# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Course.oral_written_details'
        db.delete_column('cscm_course', 'oral_written_details')

        # Deleting field 'Course.class_time_spent'
        db.delete_column('cscm_course', 'class_time_spent')

        # Adding field 'Course.class_time_spent_theory'
        db.add_column('cscm_course', 'class_time_spent_theory',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'Course.class_time_spent_analysis'
        db.add_column('cscm_course', 'class_time_spent_analysis',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'Course.class_time_spent_design'
        db.add_column('cscm_course', 'class_time_spent_design',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'Course.class_time_spent_ethics'
        db.add_column('cscm_course', 'class_time_spent_ethics',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'Course.communciation_details_num_reports'
        db.add_column('cscm_course', 'communciation_details_num_reports',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Course.communciation_details_pages'
        db.add_column('cscm_course', 'communciation_details_pages',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Course.communciation_details_num_pres'
        db.add_column('cscm_course', 'communciation_details_num_pres',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Course.communciation_details_num_mins'
        db.add_column('cscm_course', 'communciation_details_num_mins',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Course.oral_written_details'
        db.add_column('cscm_course', 'oral_written_details',
                      self.gf('django.db.models.fields.CharField')(default=',,,', max_length=20),
                      keep_default=False)

        # Adding field 'Course.class_time_spent'
        db.add_column('cscm_course', 'class_time_spent',
                      self.gf('django.db.models.fields.CharField')(default=',,,', max_length=50),
                      keep_default=False)

        # Deleting field 'Course.class_time_spent_theory'
        db.delete_column('cscm_course', 'class_time_spent_theory')

        # Deleting field 'Course.class_time_spent_analysis'
        db.delete_column('cscm_course', 'class_time_spent_analysis')

        # Deleting field 'Course.class_time_spent_design'
        db.delete_column('cscm_course', 'class_time_spent_design')

        # Deleting field 'Course.class_time_spent_ethics'
        db.delete_column('cscm_course', 'class_time_spent_ethics')

        # Deleting field 'Course.communciation_details_num_reports'
        db.delete_column('cscm_course', 'communciation_details_num_reports')

        # Deleting field 'Course.communciation_details_pages'
        db.delete_column('cscm_course', 'communciation_details_pages')

        # Deleting field 'Course.communciation_details_num_pres'
        db.delete_column('cscm_course', 'communciation_details_num_pres')

        # Deleting field 'Course.communciation_details_num_mins'
        db.delete_column('cscm_course', 'communciation_details_num_mins')


    models = {
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
            'lab_projects': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pre_reqs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'prog_assignments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'cscm.courselogentry': {
            'Meta': {'object_name': 'CourseLogEntry'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Course']"}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'evaluation_instruments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture_date': ('django.db.models.fields.DateField', [], {}),
            'lecture_no': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'topics_covered': ('django.db.models.fields.TextField', [], {}),
            'week_no': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'cscm.courseoutline': {
            'Meta': {'object_name': 'CourseOutline'},
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cscm.Course']", 'unique': 'True'}),
            'course_policies': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objectives': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'other_information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recommended_books': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_books': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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