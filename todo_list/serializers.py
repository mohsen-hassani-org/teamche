from django.utils import timezone
from rest_framework import serializers
from .models import TodoList, TodoListItem, TodoListItemTimeTrack


class TodoListItemTimeTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoListItemTimeTrack
        fields = ('id', 'start_datetime', 'end_datetime')
       

class TodoListItemSerializer(serializers.ModelSerializer):
    time_tracks = TodoListItemTimeTrackSerializer(many=True, read_only=True)
    todo_list = serializers.PrimaryKeyRelatedField(read_only=True)
    dmo = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    total_time_in_sec = serializers.SerializerMethodField()
    in_progress_from = serializers.SerializerMethodField()
    class Meta:
        model = TodoListItem
        fields = ('id', 'title', 'desc', 'todo_list', 'time_tracks', 'status',
                  'total_time_in_sec', 'dmo', 'in_progress_from',
                  'status_display', 'created_at', 'updated_at')

    def get_dmo(self, obj):
        if not obj.dmo_day:
            return {}
        return {
            'id': obj.dmo_day.id,
            'dmo_id': obj.dmo_day.dmo.id,
            'goal': obj.dmo_day.dmo.goal,
            'is_done': obj.dmo_day.done,
        }

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_total_time_in_sec(self, obj):
        time = obj.get_total_time_seconds()
        return time

    def get_in_progress_from(self, obj):
        ongoing_track = obj.get_last_ongoing_time_track()
        if not ongoing_track:
            return None
        return (timezone.now() - ongoing_track.start_datetime).seconds


class TodoListSerializer(serializers.ModelSerializer):
    items = TodoListItemSerializer(read_only=True, many=True)

    class Meta:
        model = TodoList
        fields = ('id', 'user', 'date', 'items', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')

