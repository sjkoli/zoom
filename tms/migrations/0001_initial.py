# Generated by Django 3.1.4 on 2021-06-18 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rel_type', models.CharField(max_length=20)),
                ('fw_version', models.CharField(max_length=30)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.product')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tc_id', models.CharField(max_length=30, unique=True)),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='TestExec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('testsys_ver', models.CharField(max_length=50)),
                ('testnode', models.CharField(max_length=50)),
                ('td1', models.CharField(blank=True, max_length=100, null=True)),
                ('td2', models.CharField(blank=True, max_length=100, null=True)),
                ('dut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.product')),
                ('dut_fw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.release')),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=20)),
                ('testcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.testcase')),
                ('testexec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.testexec')),
            ],
        ),
        migrations.CreateModel(
            name='TestExecTagging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.tag')),
                ('testexec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.testexec')),
            ],
        ),
        migrations.CreateModel(
            name='TestcaseTagging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.tag')),
                ('testcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.testcase')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.project'),
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_id', models.CharField(max_length=20)),
                ('comments', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('testcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms.testcase')),
            ],
        ),
    ]
