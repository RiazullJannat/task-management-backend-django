from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        date_param = self.request.query_params.get('date', None)
        title_param = self.request.query_params.get('title', None)

        if date_param is not None:
            queryset = queryset.filter(due_date=date_param)

        if title_param is not None:
            normalized_title = title_param.strip().replace('+', ' ')
            if normalized_title:
                queryset = queryset.filter(title__icontains=normalized_title)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)