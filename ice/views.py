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
