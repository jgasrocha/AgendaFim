from rest_framework import serializers
from .models import Professor, Admin, Disciplina, AgendaFixa, TrocaAgenda

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class DisciplinaSerializer(serializers.ModelSerializer):
    professor_nome = serializers.CharField(source='professor.nome', read_only=True)
    professor_foto = serializers.ImageField(source='professor.foto', read_only=True)  # Foto do professor
    professor_id = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all(), source='professor')

    class Meta:
        model = Disciplina
        fields = ['id', 'nome', 'professor_nome', 'professor_foto', 'professor_id']


class AgendaFixaSerializer(serializers.ModelSerializer):
    disciplina_nome = serializers.CharField(source='disciplina.nome', read_only=True)
    professor_nome = serializers.CharField(source='disciplina.professor.nome', read_only=True)
    professor_foto = serializers.SerializerMethodField()

    class Meta:
        model = AgendaFixa
        fields = ['dia', 'horario', 'disciplina', 'disciplina_nome', 'professor_nome', 'professor_foto']

    def get_professor_foto(self, obj):
        # Verifica se a disciplina tem um professor e se o professor tem foto
        if obj.disciplina and obj.disciplina.professor and obj.disciplina.professor.foto:
            return obj.disciplina.professor.foto.url  # Retorna a URL da imagem
        return None  # Se não houver foto, retorna `None`

# Serializer para Troca de Agenda
class TrocaAgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrocaAgenda
        fields = '__all__'