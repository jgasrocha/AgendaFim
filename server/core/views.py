# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth import authenticate
# from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Professor, Admin, Disciplina, AgendaFixa, TrocaAgenda
from .serializers import ProfessorSerializer, AdminSerializer, DisciplinaSerializer, AgendaFixaSerializer, TrocaAgendaSerializer
# import logging
from django.http import JsonResponse

# Professores
@api_view(['GET', 'POST'])
def professor_list_create(request):
    if request.method == 'GET':
        professores = Professor.objects.all()
        serializer = ProfessorSerializer(professores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfessorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def professor_detail(request, pk):
    try:
        professor = Professor.objects.get(pk=pk)
    except Professor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfessorSerializer(professor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        professor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Admins
# Admin List & Create
@api_view(['GET', 'POST'])
def admin_list_create(request):
    if request.method == 'GET':
        admins = Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        professor_id = request.data.get('professor')  # Pega o ID do professor
        if professor_id is None:
            return Response({"professor": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            professor = Professor.objects.get(pk=professor_id)
        except Professor.DoesNotExist:
            return Response({"professor": ["Professor with this ID does not exist."]}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se já existe um admin para o professor
        admin, created = Admin.objects.get_or_create(professor=professor)  
        if created:
            return Response({
                "id": admin.id,
                "professor_id": professor.id,
                "professor_nome": professor.nome
            }, status=status.HTTP_201_CREATED)

        return Response({"detail": "Admin already exists."}, status=status.HTTP_400_BAD_REQUEST)


# Admin Detail
@api_view(['DELETE'])
def admin_delete(request, pk):
    try:
        admin = Admin.objects.get(pk=pk)
    except Admin.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Admins - Check if professor is an admin
@api_view(['GET'])
def is_professor_admin(request, professor_id):
    try:
        # Verifica se existe um admin para o professor
        admin = Admin.objects.get(professor_id=professor_id)
        return Response({"is_admin": True}, status=status.HTTP_200_OK)
    except Admin.DoesNotExist:
        return Response({"is_admin": False}, status=status.HTTP_200_OK)

    # logger = logging.getLogger(__name__)

    # class ProfessorTokenObtainPairView(TokenObtainPairView):
    #     serializer_class = ProfessorTokenSerializer

    # def post(self, request, *args, **kwargs):
    #     logger.info("Received login request")
    #     return super().post(request, *args, **kwargs)



# @api_view(['GET'])
# def check_auth(request):
#     """
#     View para verificar autenticação.
#     """
#     return Response({"detail": "Autenticado com sucesso!"})

# View para listar e criar disciplinas
@api_view(['GET', 'POST'])
def disciplina_list_create(request):
    if request.method == 'GET':
        disciplinas = Disciplina.objects.all()
        serializer = DisciplinaSerializer(disciplinas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Criação de uma nova disciplina
        serializer = DisciplinaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para detalhar, atualizar ou excluir uma disciplina
@api_view(['GET', 'PUT', 'DELETE'])
def disciplina_detail(request, pk):
    try:
        disciplina = Disciplina.objects.get(pk=pk)
    except Disciplina.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DisciplinaSerializer(disciplina)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Atualizar disciplina
        serializer = DisciplinaSerializer(disciplina, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Deletar disciplina
        disciplina.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def agenda_fixa_list_create(request):
    if request.method == 'GET':
        agendas = AgendaFixa.objects.all()
        serializer = AgendaFixaSerializer(agendas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AgendaFixaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View para Troca de Agenda
@api_view(['GET', 'POST'])
def troca_agenda_list_create(request):
    if request.method == 'GET':
        trocas = TrocaAgenda.objects.all()
        serializer = TrocaAgendaSerializer(trocas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TrocaAgendaSerializer(data=request.data)
        if serializer.is_valid():
            troca = serializer.save()
            # Se a troca for aprovada, definir o horário de troca
            if troca.status == 'aprovada':
                troca.horario_troca = now()
                troca.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para detalhar/aprovar/rejeitar uma troca
@api_view(['GET', 'PUT', 'DELETE'])
def troca_agenda_detail(request, pk):
    try:
        troca = TrocaAgenda.objects.get(pk=pk)
    except TrocaAgenda.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TrocaAgendaSerializer(troca)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TrocaAgendaSerializer(troca, data=request.data)
        if serializer.is_valid():
            troca = serializer.save()
            # Se a troca for aprovada, definir o horário de troca
            if troca.status == 'aprovada':
                troca.horario_troca = now()
                troca.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        troca.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Função para reverter trocas após 24h
def reverter_trocas():
    trocas_aprovadas = TrocaAgenda.objects.filter(status='aprovada', horario_troca__isnull=False)
    for troca in trocas_aprovadas:
        if now() >= troca.horario_troca + timedelta(hours=24):
            # Reverter troca
            troca.status = 'pendente'
            troca.horario_troca = None
            troca.save()