# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'StudentProject.team_members'
        db.delete_column('cspj_studentproject', 'team_members')

        # Adding unique constraint on 'StudentProjectMilestoneEvaluation', fields ['instructor', 'student', 'milestone']
        db.create_unique('cspj_studentprojectmilestoneevaluation', ['instructor_id', 'student_id', 'milestone_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'StudentProjectMilestoneEvaluation', fields ['instructor', 'student', 'milestone']
        db.delete_unique('cspj_studentprojectmilestoneevaluation', ['instructor_id', 'student_id', 'milestone_id'])

        # Adding field 'StudentProject.team_members'
        db.add_column('cspj_studentproject', 'team_members',
                      self.gf('django.db.models.fields.TextField')(default='.'),
                      keep_default=False)


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
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joining_date': ('django.db.models.fields.DateField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cspj.student': {
            'Meta': {'ordering': "['name']", 'object_name': 'Student'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'cspj.studentproject': {
            'Meta': {'ordering': "['year', 'semester', 'title']", 'object_name': 'StudentProject'},
            'achievements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'co_supervisors': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'project_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cspj.Student']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'cspj.studentprojectlogentry': {
            'Meta': {'object_name': 'StudentProjectLogEntry'},
            'evaluation_instruments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_originator': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'issues_discussed': ('django.db.models.fields.TextField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cspj.StudentProject']"}),
            'recommendations': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'session_date': ('django.db.models.fields.DateField', [], {})
        },
        'cspj.studentprojectmilestone': {
            'Meta': {'object_name': 'StudentProjectMilestone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cspj.StudentProjectMilestoneCategory']"}),
            'milestone_deadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cspj.StudentProject']"})
        },
        'cspj.studentprojectmilestonecategory': {
            'Meta': {'object_name': 'StudentProjectMilestoneCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'milestone_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'cspj.studentprojectmilestoneevaluation': {
            'Meta': {'unique_together': "(('instructor', 'milestone', 'student'),)", 'object_name': 'StudentProjectMilestoneEvaluation'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'evaluator_confidence': ('django.db.models.fields.FloatField', [], {}),
            'execution': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cscm.Instructor']"}),
            'issue_resolution': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cspj.StudentProjectMilestone']"}),
            'presentation': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'problem_difficulty': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'solution_strength': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cspj.Student']"})
        }
    }

    complete_apps = ['cspj']