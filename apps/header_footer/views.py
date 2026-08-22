from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Header, Footer, FooterText
from .serializers import HeaderSerializer, FooterTextSerializer, FooterSerializer


class HeaderView(APIView):
    def get(self, request):
        headers = Header.objects.all()
        serializer = HeaderSerializer(headers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HeaderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HeaderDetailView(APIView):
    def get(self, request, pk):
        header = get_object_or_404(Header, pk=pk)
        serializer = HeaderSerializer(header)
        return Response(serializer.data)

    def post(self, request, pk):
        header = get_object_or_404(Header, pk=pk)
        serializer = HeaderSerializer(header, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        header = get_object_or_404(Header, pk=pk)
        header.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FooterView(APIView):
    def get(self, request):
        footers = Footer.objects.all()
        serializer = FooterSerializer(footers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FooterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FooterTextView(APIView):
    def get(self, request):
        texts = FooterText.objects.all()
        serializer = FooterTextSerializer(texts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FooterTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
