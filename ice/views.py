from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Read, StatusLog
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





def transmitter_list(request):
    reads = Read.objects.all()
    device_data = {}

    # Aggregate the data from the Read model
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
                'status': read.status  # Initialize with the current status from the database
            }

        # Update distances and their timestamps based on transmitterSerialNumber
        if read.transmitter.transmitterSerialNumber == '1000CB':
            device_data[device_uid]['distance1'] = read.distance1 if read.distance1 is not None else device_data[device_uid]['distance1']
            device_data[device_uid]['distance1_last_update'] = read.timeStampUTC
        elif read.transmitter.transmitterSerialNumber == '1000DF':
            device_data[device_uid]['distance2'] = read.distance2 if read.distance2 is not None else device_data[device_uid]['distance2']
            device_data[device_uid]['distance2_last_update'] = read.timeStampUTC
        elif read.transmitter.transmitterSerialNumber == '10012B':
            device_data[device_uid]['distance3'] = read.distance3 if read.distance3 is not None else device_data[device_uid]['distance3']
            device_data[device_uid]['distance3_last_update'] = read.timeStampUTC
        elif read.transmitter.transmitterSerialNumber == '1000ED':
            device_data[device_uid]['distance4'] = read.distance4 if read.distance4 is not None else device_data[device_uid]['distance4']
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
        position = None
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

                # Determine the status based on the position
                if position < 2000:
                    data['status'] = 'In'
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

        # Fetch the latest Read entry for the deviceUID
        current_read = reads.filter(deviceUID=device_uid).first()

        # Update the status in the database if it has changed
        if current_read and data['status'] != current_read.status:
            current_read.status = data['status']
            print(f"Device UID: {device_uid}, Status: {data['status']}")
            current_read.save()

            # Create a new log entry in the StatusLog model
            status_log = StatusLog.objects.create(
                deviceUID=device_uid,
                status=data['status']
            )

            # Print the log entry
            print(status_log)

    # Aggregate the final device data
    aggregated_reads = list(device_data.values())
    return render(request, 'ViewPage.html', {'aggregated_reads': aggregated_reads})


def status_log_view(request):
    status_logs = StatusLog.objects.all()  # Adjust this query based on your needs
    return render(request, 'status_log.html', {'status_logs': status_logs})



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def delete_read(request, device_uid):
    print(f"Received device_uid: {device_uid}")  # Debugging line
    if request.method == 'POST':
        reads = Read.objects.filter(deviceUID=device_uid)
        if reads.exists():
            reads.delete()
    return HttpResponseRedirect('/')
