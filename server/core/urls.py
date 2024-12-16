from django.urls import path
from .views import (
    agenda_fixa_list_create,
    troca_agenda_list_create,
    troca_agenda_detail,
    professor_list_create,
    professor_detail,
    admin_list_create,
    disciplina_list_create,
    disciplina_detail,
    is_professor_admin,
    admin_delete,
)
# from .views import ProfessorTokenObtainPairView, check_auth
# from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('agendas/', agenda_fixa_list_create, name='agenda-fixa-list-create'),
    path('trocas/', troca_agenda_list_create, name='troca-agenda-list-create'),
    path('trocas/<int:pk>/', troca_agenda_detail, name='troca-agenda-detail'),
    path('professores/', professor_list_create, name='professor-list-create'),
    path('professores/<int:pk>/', professor_detail, name='professor-detail'),
    path('admins/', admin_list_create, name='admin-list-create'),
    path('admins/<int:pk>/', admin_delete, name='admin-delete'),
    path('disciplinas/', disciplina_list_create, name='disciplina-list-create'),
    path('disciplinas/<int:pk>/', disciplina_detail, name='disciplina-detail'),
    path('is_professor_admin/<int:professor_id>/', is_professor_admin, name='is-professor-admin'),
    # # path('logout/', professor_logout, name='professor_logout'),
    # path('verificar-autenticacao/', verificar_autenticacao, name='verificar_autenticacao'),
    # path("login/", ProfessorTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth-check/', check_auth, name='auth_check'),
]
