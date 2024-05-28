from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Anchor
from .serializers import AnchorSerializer

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
