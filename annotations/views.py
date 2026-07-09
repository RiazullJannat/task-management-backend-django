import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, Image, Annotation
from .serializers import ProjectSerializer, ImageSerializer, AnnotationSerializer
from django.conf import settings

IMGBB_API_KEY = settings.IMGBB_API_KEY

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            title = request.data.get('title')
            description = request.data.get('description', '')
            images = request.FILES.getlist('images')

            if not title:
                return Response({'message': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

            # 1. Create Project
            project = Project.objects.create(
                title=title, 
                description=description, 
                user=request.user
            )

            # 2. Upload to ImgBB and save to DB
            order_idx = 0
            for image_file in images:
                response = requests.post(
                    "https://api.imgbb.com/1/upload",
                    data={"key": IMGBB_API_KEY},
                    files={"image": image_file.read()}
                )
                res_data = response.json()
                
                if res_data.get('success'):
                    img_info = res_data['data']
                    Image.objects.create(
                        project=project,
                        image_url=img_info['url'],
                        width=img_info['width'],
                        height=img_info['height'],
                        order_index=order_idx
                    )
                    order_idx += 1

            # 3. Return response
            serializer = self.get_serializer(project)
            return Response({'message': 'Project created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]
