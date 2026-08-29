from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# drf-spectacular импорттору
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from .models import Header, Footer, FooterText
from .serializers import HeaderSerializer, FooterTextSerializer, FooterSerializer


@extend_schema_view(
    get=extend_schema(
        tags=['header-footer'],
        summary='Header тизмесин алуу',
        operation_id='header_list',
        responses={200: HeaderSerializer(many=True)}
    ),
    post=extend_schema(
        tags=['header-footer'],
        summary='Жаңы Header түзүү',
        operation_id='header_create',
        request=HeaderSerializer,
        responses={201: HeaderSerializer, 400: OpenApiTypes.OBJECT}
    ),
)
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


@extend_schema_view(
    get=extend_schema(
        tags=['header-footer'],
        summary='Header маалыматын ID боюнча алуу',
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Header ID номери'
            )
        ],
        responses={200: HeaderSerializer, 404: OpenApiTypes.OBJECT}
    ),
    post=extend_schema(
        tags=['header-footer'],
        summary='Header маалыматын жаңыртуу',
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Header ID номери'
            )
        ],
        request=HeaderSerializer,
        responses={200: HeaderSerializer, 400: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT}
    ),
    delete=extend_schema(
        tags=['header-footer'],
        summary='Header өчүрүү',
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Header ID номери'
            )
        ],
        responses={204: None, 404: OpenApiTypes.OBJECT}
    )
)
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


@extend_schema_view(
    get=extend_schema(
        tags=['header-footer'],
        summary='Footer тизмесин алуу',
        responses={200: FooterSerializer(many=True)}
    ),
    post=extend_schema(
        tags=['header-footer'],
        summary='Жаңы Footer түзүү',
        request=FooterSerializer,
        responses={201: FooterSerializer, 400: OpenApiTypes.OBJECT}
    )
)
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


@extend_schema_view(
    get=extend_schema(
        tags=['header-footer'],
        summary='FooterText тизмесин алуу',
        responses={200: FooterTextSerializer(many=True)}
    ),
    post=extend_schema(
        tags=['header-footer'],
        summary='Жаңы FooterText түзүү',
        request=FooterTextSerializer,
        responses={201: FooterTextSerializer, 400: OpenApiTypes.OBJECT}
    )
)
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