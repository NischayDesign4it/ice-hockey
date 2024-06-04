from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Transmitter
from .serializers import TransmitterSerializer


@api_view(['POST'])
def create_transmitter(request):
    if request.method == 'POST':
        # Extract data from the request
        transmitter_serial_number = request.data.get('transmitterSerialNumber', '')

        try:
            # Try to retrieve a single transmitter with the provided serial number
            transmitter = Transmitter.objects.get(transmitterSerialNumber=transmitter_serial_number)

            # If a transmitter is found, update it with the provided data
            serializer = TransmitterSerializer(transmitter, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Transmitter.DoesNotExist:
            # If no transmitter with the provided serial number exists, create a new one
            serializer = TransmitterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Transmitter.MultipleObjectsReturned:
            # If multiple transmitters with the provided serial number exist, handle the error
            return Response({'message': 'Multiple transmitters found for the given serial number'},
                            status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


from django.shortcuts import render
from .models import Transmitter

def transmitter_list(request):
    transmitters = Transmitter.objects.all()
    return render(request, 'ViewPage.html', {'transmitters': transmitters})






