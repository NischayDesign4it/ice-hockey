from rest_framework import serializers
from .models import Anchor, TagDistance

class TagDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagDistance
        fields = ['deviceID', 'TimeStampUTC', 'distance']

class AnchorSerializer(serializers.ModelSerializer):
    tag_distances = TagDistanceSerializer(many=True)

    class Meta:
        model = Anchor
        fields = ['anchorID', 'tag_distances']

    def create(self, validated_data):
        tag_distances_data = validated_data.pop('tag_distances')
        anchor = Anchor.objects.create(**validated_data)
        for tag_data in tag_distances_data:
            TagDistance.objects.create(anchor=anchor, **tag_data)
        return anchor
