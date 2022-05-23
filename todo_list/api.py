from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    RetrieveModelMixin, ListModelMixin, CreateModelMixin,
    UpdateModelMixin, DestroyModelMixin
)
from .models import TodoList, TodoListItem, TodoListItemTimeTrack
from .serializers import TodoListSerializer, TodoListItemSerializer, TodoListItemTimeTrackSerializer


class TodoListViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    serializer_class = TodoListSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'date'

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        queryset = TodoList.objects.filter(user=self.request.user)
        if date_from:
            queryset.filter(date__gte=date_from)
        if date_to:
            queryset.filter(date__lte=date_to)
        return queryset

    def get_object(self):
        date = self.kwargs.get('date')
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError as ex:
            date = datetime.now().date()
        return TodoList.objects.get_todo_list(self.request.user, date)

   


        
class TodoListItemViewSet(ModelViewSet):
    queryset = TodoListItem.objects.all()
    serializer_class = TodoListItemSerializer
    permission_classes = (IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        self.todo_list_date = kwargs.pop('todo_list_date', None)
        return super().dispatch(request, *args, **kwargs)

    def get_todo_list(self):
        try:
            date = datetime.strptime(self.todo_list_date, "%Y-%m-%d").date()
        except ValueError as ex:
            date = datetime.now().date()
        return TodoList.objects.get_todo_list(self.request.user, date)

    def get_queryset(self):
        user = self.request.user
        todo_list = self.get_todo_list()
        return super().get_queryset().filter(todo_list=todo_list,
                                             todo_list__user=user)

    def perform_create(self, serializer):
        todo_list = self.get_todo_list()
        serializer.save(todo_list=todo_list)
        
    @action(detail=True, url_path='start')
    def start_time_track(self, request, pk=None):
        todo_list_item = self.get_object()
        todo_list_item.start_task()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='end')
    def end_time_track(self, request, pk=None):
        todo_list_item = self.get_object()
        todo_list_item.finish_task()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='done')
    def mark_item_done(self, request, pk=None):
        todo_list_item = self.get_object()
        todo_list_item.done_task()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='undone')
    def mark_item_undone(self, request, pk=None):
        todo_list_item = self.get_object()
        todo_list_item.undone_task()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, url_path='play-pause')
    def toggle_start_stop(self, request, pk=None):
        todo_list_item = self.get_object()
        todo_list_item.toggle_start_stop()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, url_path='delete')
    def delete_task(self, request, pk=None):
        todo_list_item = self.get_object()
        todo_list_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


