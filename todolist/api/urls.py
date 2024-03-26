from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'todo-list', views.TodoListViewSet)
router.register(r'todo-item', views.TodoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]