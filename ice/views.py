from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Read
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Transmitter
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TransmitterSerializer, ReadSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# @api_view(['POST'])
# def create_transmitter(request):
#     if request.method == 'POST':
#         # Extract data from the request
#         transmitter_serial_number = request.data.get('transmitterSerialNumber', '')
#
#         try:
#             # Try to retrieve a single transmitter with the provided serial number
#             transmitter = Transmitter.objects.get(transmitterSerialNumber=transmitter_serial_number)
#
#             # If a transmitter is found, update it with the provided data
#             serializer = TransmitterSerializer(transmitter, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         except Transmitter.DoesNotExist:
#             # If no transmitter with the provided serial number exists, create a new one
#             serializer = TransmitterSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         except Transmitter.MultipleObjectsReturned:
#             # If multiple transmitters with the provided serial number exist, handle the error
#             return Response({'message': 'Multiple transmitters found for the given serial number'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#     return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Transmitter
from .serializers import TransmitterSerializer
import json

@api_view(['POST'])
def create_transmitter(request):
    if request.method == 'POST':
        try:
            # Try to parse JSON data from the request body
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # If parsing fails, assume it's plain text and use the request body directly
            data = request.body.decode('utf-8').strip()

        try:
            # Try to retrieve a single transmitter with the provided serial number
            if isinstance(data, dict):
                transmitter_serial_number = data.get('transmitterSerialNumber', '')
            else:
                # For plain text data, assume it's the serial number itself
                transmitter_serial_number = data
            transmitter = Transmitter.objects.get(transmitterSerialNumber=transmitter_serial_number)

            # If a transmitter is found, update it with the provided data
            serializer = TransmitterSerializer(transmitter, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Transmitter.DoesNotExist:
            # If no transmitter with the provided serial number exists, create a new one
            serializer = TransmitterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Transmitter.MultipleObjectsReturned:
            # If multiple transmitters with the provided serial number exist, handle the error
            return Response({'message': 'Multiple transmitters found for the given serial number'},
                            status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def transmitter_list(request):
    transmitters = Transmitter.objects.all()
    return render(request, 'ViewPage.html', {'transmitters': transmitters})






