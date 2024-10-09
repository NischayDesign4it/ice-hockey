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
from datetime import timedelta, datetime
from django.utils.timezone import now


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

#     for read in reads:
#         device_uid = read.deviceUID

#         if device_uid not in device_data:
#             device_data[device_uid] = {
#                 'deviceUID': device_uid,
#                 'distance1': None,
#                 'distance2': None,
#                 'distance3': None,
#                 'distance4': None,
#                 'position': None,
#                 'timeStampUTC': read.timeStampUTC,
#                 'lastTimeStamp': read.lastTimeStamp,  # Initialize with the value from the read
#                 'status': 'Out'
#             }

#         # Update distances based on transmitterSerialNumber
#         if read.transmitter.transmitterSerialNumber == '1000CB':
#             device_data[device_uid]['distance1'] = read.distance1 if read.distance1 is not None else device_data[device_uid]['distance1']
#         elif read.transmitter.transmitterSerialNumber == '1000DF':
#             device_data[device_uid]['distance2'] = read.distance2 if read.distance2 is not None else device_data[device_uid]['distance2']
#         elif read.transmitter.transmitterSerialNumber == '10012B':
#             device_data[device_uid]['distance3'] = read.distance3 if read.distance3 is not None else device_data[device_uid]['distance3']
#         elif read.transmitter.transmitterSerialNumber == '1000ED':
#             device_data[device_uid]['distance4'] = read.distance4 if read.distance4 is not None else device_data[device_uid]['distance4']
        

#         device_data[device_uid]['lastTimeStamp'] = read.lastTimeStamp


#         # Update timestamps if the current read's timestamp is newer
#         if read.timeStampUTC > device_data[device_uid]['timeStampUTC']:
#             device_data[device_uid]['timeStampUTC'] = read.timeStampUTC
        

#     # Calculate position and update status
#     for device_uid, data in device_data.items():
#         d2 = data['distance2']
#         d3 = data['distance3']
#         if d2 is not None and d3 is not None:
#             l = 5000  # Predefined distance
#             value_under_sqrt = (d3 ** 2 - ((l ** 2 - d2 ** 2 + d3 ** 2) ** 2) / (4 * l ** 2))

#             if value_under_sqrt >= 0:
#                 position = math.sqrt(value_under_sqrt)
#                 data['position'] = position

#                 if position < 2000:
#                     data['status'] = 'In'

#                     read.lastTimeStamp = now()  # Get current timestamp
#                     read.save()  # Update in the database
#                     data['lastTimeStamp'] = read.lastTimeStamp  # Update in-memory
#                     print(f"LastTime (in):{device_uid} {data['lastTimeStamp']}")

#                 elif position >= 2000:
#                     current_time = now()  # Current time for comparison
#                     last_time = data['lastTimeStamp']  # Use in-memory last timestamp

#                     # If lastTimeStamp is present, calculate the time difference
#                     if last_time:
#                         time_difference = current_time - last_time
#                         print(f"Current time: {current_time}")
#                         print(f"Last time: {last_time}")
#                         print(f"Time difference: {time_difference}")

#                         # If time difference is 10 seconds or more, mark as 'Out'
#                         if time_difference >= timedelta(seconds=10):
#                             data['status'] = 'Out'
#                         else:
#                             data['status'] = 'In'
#                     else:
#                         print(f"No lastTimeStamp available for deviceUID {device_uid}")

#     aggregated_reads = list(device_data.values())
#     return render(request, 'ViewPage.html', {'aggregated_reads': aggregated_reads})


def transmitter_list(request):
    reads = Read.objects.all()
    device_data = {}

    for read in reads:
        device_uid = read.deviceUID

        if device_uid not in device_data:
            device_data[device_uid] = {
                'deviceUID': device_uid,
                'distance1': None,
                'distance2': None,
                'distance3': None,
                'distance4': None,
                'position': None,
                'timeStampUTC': read.timeStampUTC,
                'lastTimeStamp': read.lastTimeStamp,
                'status': 'Out'
            }

        # Update distances and their timestamps based on transmitterSerialNumber
        if read.transmitter.transmitterSerialNumber == '1000CB':
            device_data[device_uid]['distance1'] = read.distance1 if read.distance1 is not None else \
            device_data[device_uid]['distance1']
            device_data[device_uid]['distance1_last_update'] = read.timeStampUTC
        elif read.transmitter.transmitterSerialNumber == '1000DF':
            device_data[device_uid]['distance2'] = read.distance2 if read.distance2 is not None else \
            device_data[device_uid]['distance2']
            device_data[device_uid]['distance2_last_update'] = read.timeStampUTC
        elif read.transmitter.transmitterSerialNumber == '10012B':
            device_data[device_uid]['distance3'] = read.distance3 if read.distance3 is not None else \
            device_data[device_uid]['distance3']
            device_data[device_uid]['distance3_last_update'] = read.timeStampUTC
        elif read.transmitter.transmitterSerialNumber == '1000ED':
            device_data[device_uid]['distance4'] = read.distance4 if read.distance4 is not None else \
            device_data[device_uid]['distance4']
            device_data[device_uid]['distance4_last_update'] = read.timeStampUTC

        # Update last timestamp
        device_data[device_uid]['lastTimeStamp'] = read.lastTimeStamp

        # Update timestamps if the current read's timestamp is newer
        if read.timeStampUTC > device_data[device_uid]['timeStampUTC']:
            device_data[device_uid]['timeStampUTC'] = read.timeStampUTC

    # Calculate position and update status
    for device_uid, data in device_data.items():
        d2 = data['distance2']
        d3 = data['distance3']
        if d2 is not None and d3 is not None:
            l = 5000  # Predefined distance
            value_under_sqrt = (d3 ** 2 - ((l ** 2 - d2 ** 2 + d3 ** 2) ** 2) / (4 * l ** 2))
            if value_under_sqrt >= 0:
                position = math.sqrt(value_under_sqrt)
            elif d2 < 2000:
                position = d2
            elif d3 < 2000:
                position = d3

            if position is not None:
                data['position'] = position

                if position < 2000:
                    data['status'] = 'In'
                    read.lastTimeStamp = now()
                    read.save()
                    data['lastTimeStamp'] = read.lastTimeStamp
                elif position >= 2000:
                    current_time = now()
                    last_time = data['lastTimeStamp']

                    if last_time:
                        time_difference = current_time - last_time
                        if time_difference >= timedelta(seconds=10):
                            data['status'] = 'Out'
                        else:
                            data['status'] = 'In'

        # Check if any distance hasn't been updated for 10 seconds
        current_time = now()
        for dist_key in ['timeStampUTC']:
            last_update = data[dist_key]
            if last_update and (current_time - last_update) >= timedelta(seconds=10):
                data['status'] = 'Out'
                break  # No need to check further if one distance is already timed out

    aggregated_reads = list(device_data.values())
    return render(request, 'ViewPage.html', {'aggregated_reads': aggregated_reads})


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def delete_read(request, device_uid):
    print(f"Received device_uid: {device_uid}")  # Debugging line
    if request.method == 'POST':
        reads = Read.objects.filter(deviceUID=device_uid)
        if reads.exists():
            reads.delete()
    return HttpResponseRedirect('/')