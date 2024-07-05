from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from service_registrar.mixins import ServiceAddressMixin
import requests
User = get_user_model()

class CreateUserView(ServiceAddressMixin,generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        role = request.data.get('type', 'patient')
        if role == 'doctor':
            try:
                self.get_service_address('doctors')
            except Exception as e:
                return self.response_from_exception(e)
            status = requests.post(f"{self.url}/api/doctors", json=request.data)
            if status.status_code != 201:
                return Response(status.json(), status=status.status_code)

        elif role == 'patient':
            try:
                self.get_service_address('patients')
            except Exception as e:
                return self.response_from_exception(e)
            status = requests.post(f"{self.url}/api/patients", json=request.data)
            if status.status_code != 201:
                return Response(status.json(), status=status.status_code)

        return super().post(request, *args, **kwargs)