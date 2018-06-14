from rest_framework.generics import CreateAPIView, UpdateAPIView

from .models import DemoModel
from .serializers import DemoModelSerializer


class DemoCreateView(CreateAPIView):
    serializer_class = DemoModelSerializer


class DemoUpdateView(UpdateAPIView):
    queryset = DemoModel.objects.all()
    serializer_class = DemoModelSerializer
