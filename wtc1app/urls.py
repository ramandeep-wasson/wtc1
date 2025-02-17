from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather, name='weather'),  # Weather and tasks
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('chat/', views.chatbot_ui, name='chatbot_ui'),  # Chat UI page
    path('api/message/', views.chatbot_response, name='chatbot_response'),
]
