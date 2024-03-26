from rest_framework import serializers
from .models import *

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = '__all__'

class TodoItemSerializer(serializers.ModelSerializer):
    todo_list = TodoListSerializer()
    class Meta:
        model = TodoItem
        fields = '__all__'

class TodoItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'