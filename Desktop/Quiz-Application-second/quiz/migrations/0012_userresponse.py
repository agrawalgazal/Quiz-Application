# Generated by Django 4.2.18 on 2025-02-05 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0011_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('user_response_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_ans', models.CharField(max_length=200)),
                ('question_response_time', models.IntegerField()),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
