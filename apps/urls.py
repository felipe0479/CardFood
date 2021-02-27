from django.urls import path
from . import views

urlpatterns = [
    path("client/<int:id>",views.get_client),
    path("bonus/<int:id>",views.get_bonus_client),
    path("delete_bonus/<int:id>",views.delete_bonus_client),
    path("create_bonus/<int:id>/<str:emp>/<int:pts>",views.create_bonus_client),
    path("create_card/<int:id>/<str:code>",views.create_card),
    path("deactivate_card/<int:id>",views.deactivate_card),
    path("client_by_card/<str:id>",views.client_by_card),
    path("bonus_by_tgm/<int:id>",views.bonus_by_id),
    
]