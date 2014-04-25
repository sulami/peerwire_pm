# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Skill'
        db.delete_table(u'projects_skill')

        # Deleting model 'UserSkill'
        db.delete_table(u'projects_userskill')


        # Changing field 'UserLang.level'
        db.alter_column(u'projects_userlang', 'level', self.gf('django.db.models.fields.CharField')(max_length=8))
        # Removing M2M table for field skills on 'Project'
        db.delete_table(db.shorten_name(u'projects_project_skills'))


        # Changing field 'Project.status'
        db.alter_column(u'projects_project', 'status', self.gf('django.db.models.fields.CharField')(max_length=8))

        # Changing field 'Project.level'
        db.alter_column(u'projects_project', 'level', self.gf('django.db.models.fields.CharField')(max_length=8))

    def backwards(self, orm):
        # Adding model 'Skill'
        db.create_table(u'projects_skill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'projects', ['Skill'])

        # Adding model 'UserSkill'
        db.create_table(u'projects_userskill', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.User'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Skill'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'projects', ['UserSkill'])


        # Changing field 'UserLang.level'
        db.alter_column(u'projects_userlang', 'level', self.gf('django.db.models.fields.CharField')(max_length=10))
        # Adding M2M table for field skills on 'Project'
        m2m_table_name = db.shorten_name(u'projects_project_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('skill', models.ForeignKey(orm[u'projects.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'skill_id'])


        # Changing field 'Project.status'
        db.alter_column(u'projects_project', 'status', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'Project.level'
        db.alter_column(u'projects_project', 'level', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'projects.credit': {
            'Meta': {'object_name': 'Credit'},
            'ack': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.User']"})
        },
        u'projects.lang': {
            'Meta': {'object_name': 'Lang'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'change_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'del_q': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'del_q'", 'blank': 'True', 'to': u"orm['projects.User']"}),
            'del_t': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'langs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.Lang']", 'symmetrical': 'False', 'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects_owned'", 'symmetrical': 'False', 'to': u"orm['projects.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'seeking': ('django.db.models.fields.CharField', [], {'default': "'No'", 'max_length': '3'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '8'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'projects_workingon'", 'blank': 'True', 'to': u"orm['projects.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'projects.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'del_t': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'premium': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'projects.userlang': {
            'Meta': {'object_name': 'UserLang'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Lang']"}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.User']"})
        }
    }

    complete_apps = ['projects']