from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True, null=True)
    senha = models.CharField(max_length=128, null=True)
    foto = models.ImageField(upload_to='fotos_professores/', blank=True, null=True)

    def __str__(self):
        return self.nome

    @property
    def is_admin(self):
        return Admin.objects.filter(professor=self).exists()

class Admin(models.Model):
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Admin: {self.professor.nome if self.professor else "Sem Professor"}'

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="disciplinas")

    def __str__(self):
        return self.nome

class AgendaFixa(models.Model):
    dia = models.CharField(max_length=10, null=True)  # Exemplo: 'Seg', 'Ter'
    horario = models.TimeField()
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dia} {self.horario} - {self.disciplina.nome}"
    def get_professor(self):
        return self.disciplina.professor

    # Método para obter a foto do professor
    def get_professor_foto(self):
        return self.disciplina.professor.foto if self.disciplina.professor.foto else None

class TrocaAgenda(models.Model):
    agenda_original = models.ForeignKey(AgendaFixa, on_delete=models.CASCADE, related_name='trocas', null=True)
    professor_solicitante = models.ForeignKey('Professor', on_delete=models.CASCADE, null=True)
    nova_disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=[('pendente', 'Pendente'), ('aprovada', 'Aprovada'), ('rejeitada', 'Rejeitada')], default='pendente')
    horario_troca = models.DateTimeField(null=True, blank=True)  # Para gerenciar o timer

    def __str__(self):
        return f"Troca: {self.professor_solicitante.nome} -> {self.nova_disciplina.nome} ({self.status})"