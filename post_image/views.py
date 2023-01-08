from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Image
from .serializers import ImageSerializer, ImagePostSerializer
from .filters import ImageFilter
from .permissions import IsAuthorOrReadOnly


class ImageList(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ImageFilter
    http_method_names = ['get', 'put', 'head', 'delete']



class UploadImage(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Image.objects.all()
    serializer_class = ImagePostSerializer
    model = Image



    def create(self, request, *args, **kwargs):
        serializer_for_image = self.serializer_class(data=request.data)
        serializer_for_image.is_valid(raise_exception=True)
        if serializer_for_image.is_valid():
            serializer_for_image.save(user=request.user, author=request.user.full_name)
            return Response({"Success": "Изображение загружено"}, status=status.HTTP_201_CREATED)
        return Response(serializer_for_image.errors, status=status.HTTP_400_BAD_REQUEST)
