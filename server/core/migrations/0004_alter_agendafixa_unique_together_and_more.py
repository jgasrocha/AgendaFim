# Generated by Django 5.1.4 on 2024-12-15 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_professor_email_professor_senha'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='agendafixa',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='trocaagenda',
            name='agenda_fixa_original',
        ),
        migrations.RemoveField(
            model_name='trocaagenda',
            name='aprovada',
        ),
        migrations.RemoveField(
            model_name='trocaagenda',
            name='dia_novo',
        ),
        migrations.RemoveField(
            model_name='trocaagenda',
            name='horario_novo',
        ),
        migrations.RemoveField(
            model_name='trocaagenda',
            name='justificativa',
        ),
        migrations.RemoveField(
            model_name='trocaagenda',
            name='professor',
        ),
        migrations.AddField(
            model_name='agendafixa',
            name='dia',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='trocaagenda',
            name='agenda_original',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trocas', to='core.agendafixa'),
        ),
        migrations.AddField(
            model_name='trocaagenda',
            name='horario_troca',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trocaagenda',
            name='nova_disciplina',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.disciplina'),
        ),
        migrations.AddField(
            model_name='trocaagenda',
            name='professor_solicitante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.professor'),
        ),
        migrations.AddField(
            model_name='trocaagenda',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('aprovada', 'Aprovada'), ('rejeitada', 'Rejeitada')], default='pendente', max_length=10),
        ),
        migrations.RemoveField(
            model_name='agendafixa',
            name='descricao_local',
        ),
        migrations.RemoveField(
            model_name='agendafixa',
            name='dia_semana',
        ),
        migrations.RemoveField(
            model_name='agendafixa',
            name='local_foto',
        ),
    ]