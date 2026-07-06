from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from task_management_backend.response_utils import error_response, success_response
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        date_param = self.request.query_params.get('date', None)
        if date_param is not None:
            queryset = queryset.filter(due_date=date_param)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response('Tasks retrieved successfully', serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(user=request.user)
            return success_response(
                'Task created successfully',
                self.get_serializer(task).data,
                status.HTTP_201_CREATED,
            )
        return error_response('Task creation failed', serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response('Task retrieved successfully', serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response('Task updated successfully', serializer.data)
        return error_response('Task update failed', serializer.errors, status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response('Task deleted successfully', None)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)