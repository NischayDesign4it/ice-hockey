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
from django.shortcuts import render, redirect, HttpResponseRedirect




import json


from django.utils import timezone


# @api_view(['POST'])
# def create_transmitter(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             transmitter_serial_number = data.get('transmitterSerialNumber', '')
#             existing_transmitter = Transmitter.objects.filter(transmitterSerialNumber=transmitter_serial_number).first()
#
#             if existing_transmitter:
#                 serializer = TransmitterSerializer(existing_transmitter, data=data)
#             else:
#                 serializer = TransmitterSerializer(data=data)
#
#             if serializer.is_valid():
#                 # Update distance and timestamp
#                 serializer.save()
#                 update_read_timestamp(serializer.instance.reads.all())
#
#                 return Response(serializer.data,
#                                 status=status.HTTP_200_OK if existing_transmitter else status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         except Exception as e:
#             return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#     return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#
# def update_read_timestamp(reads):
#     """
#     Update the timestamp for all reads passed as argument.
#     """
#     current_timestamp = timezone.now()
#     for read in reads:
#         read.timeStampUTC = current_timestamp
#         read.save()


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
            data = json.loads(request.body)
            transmitter_serial_number = data.get('transmitterSerialNumber', '')
            existing_transmitter = Transmitter.objects.filter(transmitterSerialNumber=transmitter_serial_number).first()

            if existing_transmitter:
                serializer = TransmitterSerializer(existing_transmitter, data=data)
            else:
                serializer = TransmitterSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK if existing_transmitter else status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




def delete_read(request, device_uid):
    reads = Read.objects.filter(deviceUID=device_uid)
    if reads.exists():
        reads.delete()
    return HttpResponseRedirect('/')


from django.shortcuts import render
from datetime import datetime, timedelta

def transmitter_list(request):
    current_time = datetime.utcnow()
    threshold_time = current_time - timedelta(seconds=10)
    filtered_reads = Read.objects.filter(timeStampUTC__gte=threshold_time)
    return render(request, 'ViewPage.html', {'filtered_reads': filtered_reads})





# # views.py
# import math
# from django.shortcuts import render
# from .models import DeviceRead
#
# def calculate_position(d1, d2):
#     if d1 is not None and d2 is not None:
#         try:
#             position = math.sqrt((d1**2 + d2**2 - 100) / 2)
#             return position
#         except ValueError:
#             return "N/A"
#     return "N/A"
#
# def device_distances_view(request):
#     aggregated_reads = DeviceRead.objects.all()
#
#     for read in aggregated_reads:
#         read.position = calculate_position(read.distance1, read.distance2)
#
#     return render(request, 'device_distances.html', {'aggregated_reads': aggregated_reads})
