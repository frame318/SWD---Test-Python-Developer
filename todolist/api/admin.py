from django.contrib import admin
from .models import TodoList, TodoItem
# Register your models here.

@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed', 'created_at', 'updated_at')

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('todo_list', 'title', 'description', 'completed', 'created_at', 'updated_at')