from django.urls import path
from . import views

app_name = 'styleboard'

urlpatterns = [
    path('', views.style_board_view, name='view'),
    path('add/<int:product_id>/', views.add_to_board, name='add'),
    path('remove/<int:product_id>/', views.remove_from_board, name='remove'),
]