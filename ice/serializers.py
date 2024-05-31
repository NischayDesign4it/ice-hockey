from rest_framework import serializers
from rest_framework import serializers
from .models import Transmitter, Read

class ReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Read
        fields = ['timeStampUTC', 'deviceUID', 'manufacturerName', 'distance', 'count']
        extra_kwargs = {
            'distance': {'required': False},
            'count': {'required': False}
        }

class TransmitterSerializer(serializers.ModelSerializer):
    reads = ReadSerializer(many=True)

    class Meta:
        model = Transmitter
        fields = ['transmitterSerialNumber', 'nodeType', 'reads', 'allCount']


    def create(self, validated_data):
        reads_data = validated_data.pop('reads')
        transmitter = Transmitter.objects.create(**validated_data)
        for read_data in reads_data:
            Read.objects.create(transmitter=transmitter, **read_data)
        return transmitter

    def update(self, instance, validated_data):
        reads_data = validated_data.pop('reads', None)
        if reads_data:
            for read_data in reads_data:
                Read.objects.create(transmitter=instance, **read_data)
        return instance
