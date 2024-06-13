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
import math





import json


from django.utils import timezone



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



# def transmitter_list(request):
#     reads = Read.objects.all()
#     device_data = {}
#
#     for read in reads:
#         if read.deviceUID not in device_data:
#             device_data[read.deviceUID] = {
#                 'deviceUID': read.deviceUID,
#                 'distance1': None,
#                 'distance2': None,
#                 'distance3': None,
#                 'distance4': None,
#                 'timeStampUTC': read.timeStampUTC
#             }
#
#         if read.transmitter.transmitterSerialNumber == '1000CB':
#             device_data[read.deviceUID]['distance1'] = read.distance1 if read.distance1 is not None else device_data[read.deviceUID]['distance1']
#         elif read.transmitter.transmitterSerialNumber == '1000DF':
#             device_data[read.deviceUID]['distance2'] = read.distance2 if read.distance2 is not None else device_data[read.deviceUID]['distance2']
#         elif read.transmitter.transmitterSerialNumber == '10012B':
#             device_data[read.deviceUID]['distance3'] = read.distance3 if read.distance3 is not None else device_data[read.deviceUID]['distance3']
#         elif read.transmitter.transmitterSerialNumber == '1000ED':
#             device_data[read.deviceUID]['distance4'] = read.distance4 if read.distance4 is not None else device_data[read.deviceUID]['distance4']
#
#         if read.timeStampUTC > device_data[read.deviceUID]['timeStampUTC']:
#             device_data[read.deviceUID]['timeStampUTC'] = read.timeStampUTC
#
#     aggregated_reads = list(device_data.values())
#
#     return render(request, 'ViewPage.html', {'aggregated_reads': aggregated_reads})



from django.shortcuts import render
import math

def transmitter_list(request):
    reads = Read.objects.all()
    device_data = {}

    for read in reads:
        if read.deviceUID not in device_data:
            device_data[read.deviceUID] = {
                'deviceUID': read.deviceUID,
                'distance1': None,
                'distance2': None,
                'distance3': None,
                'distance4': None,
                'timeStampUTC': read.timeStampUTC
            }

        if read.transmitter.transmitterSerialNumber == '1000CB':
            device_data[read.deviceUID]['distance1'] = read.distance1 if read.distance1 is not None else device_data[read.deviceUID]['distance1']
        elif read.transmitter.transmitterSerialNumber == '1000DF':
            device_data[read.deviceUID]['distance2'] = read.distance2 if read.distance2 is not None else device_data[read.deviceUID]['distance2']
        elif read.transmitter.transmitterSerialNumber == '10012B':
            device_data[read.deviceUID]['distance3'] = read.distance3 if read.distance3 is not None else device_data[read.deviceUID]['distance3']
        elif read.transmitter.transmitterSerialNumber == '1000ED':
            device_data[read.deviceUID]['distance4'] = read.distance4 if read.distance4 is not None else device_data[read.deviceUID]['distance4']

        if read.timeStampUTC > device_data[read.deviceUID]['timeStampUTC']:
            device_data[read.deviceUID]['timeStampUTC'] = read.timeStampUTC

    # Calculate position dynamically for each device
    for device_uid, data in device_data.items():
        d1 = data['distance1']
        d2 = data['distance2']
        if d1 is not None and d2 is not None:
            value_under_sqrt = (d1 ** 2 + d2 ** 2 - 100) / 2
            if value_under_sqrt >= 0:
                position = math.sqrt(value_under_sqrt)
                data['position'] = position
                print(data['position'])
                print(data['position'])
            else:
                data['position'] = None



        else:
            data['position'] = None  # Handle case where either d1 or d2 is None

    aggregated_reads = list(device_data.values())

    return render(request, 'ViewPage.html', {'aggregated_reads': aggregated_reads})



def delete_read(request, device_uid):
    reads = Read.objects.filter(deviceUID=device_uid)
    if reads.exists():
        reads.delete()
    return HttpResponseRedirect('/')
