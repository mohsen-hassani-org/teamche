from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .api import TodoListViewSet, TodoListItemViewSet


app_name = 'todo_list'


todo_list_router = DefaultRouter()
todo_list_router.register(r'todo-list', TodoListViewSet, basename='todo_list')
todo_list_domain_router = routers.NestedSimpleRouter(todo_list_router, r'todo-list', lookup='todo_list')
todo_list_domain_router.register(r'items', TodoListItemViewSet, basename='todo_list-items')


urlpatterns = [
    path('api/v1/', include(todo_list_router.urls)),
    path('api/v1/', include(todo_list_domain_router.urls)),
]
