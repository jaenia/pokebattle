from django.urls import path

from . import views

app_name = 'battles'
urlpatterns = [
    path('add/', views.BattleCreate.as_view(), name='battle_create'),
    path('<int:pk>', views.BattleDetail.as_view(), name='battle_detail'),
]
