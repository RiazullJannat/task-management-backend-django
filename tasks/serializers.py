from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    def to_internal_value(self, data):
        if isinstance(data, dict):
            normalized = data.copy()
            status = normalized.get('status')
            if isinstance(status, str):
                normalized['status'] = {
                    'PENDING': 'TODO',
                    'IN_PROGRESS': 'IN_PROGRESS',
                    'INPROGRESS': 'IN_PROGRESS',
                    'DONE': 'DONE',
                    'TODO': 'TODO',
                }.get(status.strip().upper(), status.strip().upper())

            priority = normalized.get('priority')
            if isinstance(priority, str):
                normalized['priority'] = {
                    'LOW': 'LOW',
                    'MEDIUM': 'MEDIUM',
                    'HIGH': 'HIGH',
                    'LOWER': 'LOW',
                    'NORMAL': 'MEDIUM',
                }.get(priority.strip().upper(), priority.strip().upper())

            tags = normalized.get('tags')
            if isinstance(tags, str):
                normalized['tags'] = [tag.strip() for tag in tags.split(',') if tag.strip()]

            data = normalized

        return super().to_internal_value(data)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'status', 'priority', 'due_date', 'tags', 'position', 'created_at', 'updated_at']