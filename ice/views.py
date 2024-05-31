from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Anchor
from .serializers import AnchorSerializer
from .models import Read, Transmitter
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import TransmitterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Transmitter
from .serializers import TransmitterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transmitter
from .serializers import TransmitterSerializer, ReadSerializer

class AnchorTagInfoView(APIView):
    def post(self, request):
        serializer = AnchorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        anchors = Anchor.objects.all()
        serializer = AnchorSerializer(anchors, many=True)
        return Response(serializer.data)


# myapp/views.py
import requests  # Add this import statement
from django.shortcuts import render

def anchor_tag_info(request):
    # Fetch data from the API
    api_url = 'http://127.0.0.1:8000/api/anchor-tag-info/'
    response = requests.get(api_url)
    data = response.json()

    # Pass data to the template
    return render(request, 'ViewPage.html', {'data': data})









@api_view(['POST'])
@csrf_exempt
def create_transmitter(request):
    if request.method == 'POST':
        transmitter_serial_number = request.data.get('transmitterSerialNumber')
        try:
            transmitter = Transmitter.objects.get(transmitterSerialNumber=transmitter_serial_number)
            serializer = TransmitterSerializer(transmitter, data=request.data, partial=True)
        except Transmitter.DoesNotExist:
            serializer = TransmitterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TransmitterAPIView(APIView):
    def get(self, request, transmitter_serial_number=None):
        if transmitter_serial_number:
            try:
                transmitter = Transmitter.objects.get(transmitterSerialNumber=transmitter_serial_number)
                serializer = TransmitterSerializer(transmitter)
                return Response(serializer.data)
            except Transmitter.DoesNotExist:
                return Response({"detail": "Transmitter with given Serial Number does not exist."}, status=status.HTTP_404_NOT_FOUND)
        else:
            transmitters = Transmitter.objects.all()
            serializer = TransmitterSerializer(transmitters, many=True)
            return Response(serializer.data)

