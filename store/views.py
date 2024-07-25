from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from store.filters import NftFilter
from store.models import Nft, Category
from store.serializers import NftSerializer, CatSerializer


class NftPagination(PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):
        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class NftViewSet(APIView):

    @swagger_auto_schema(
        operation_description="Получение всех NFT",
        manual_parameters=[
            openapi.Parameter('min_price', in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                              description='Минимальная цена'),
            openapi.Parameter('max_price', in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                              description='Максимальная цена'),
            openapi.Parameter('category', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Категория')
        ],
        responses={200: NftSerializer(many=True)}
    )
    def get(self, request):
        nft = Nft.objects.all().order_by('id')
        filters = NftFilter(request.GET, queryset=nft)
        if filters.is_valid():
            nft = filters.qs
        paginator = NftPagination()
        page = paginator.paginate_queryset(nft, request)
        if page is not None:
            serializer = NftSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = NftSerializer(nft, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Создание нового NFT",
        request_body=NftSerializer,
        responses={201: NftSerializer}
    )
    def post(self, request):
        serializer = NftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NftViewDetail(APIView):
    @swagger_auto_schema(
        operation_description="Получение NFT по id",
        responses={200: NftSerializer, 404: 'NFT не найдена'}
    )
    def get(self, request, pk):
        try:
            nft = Nft.objects.get(pk=pk)
            serializer = NftSerializer(nft)
            return Response(serializer.data)
        except Nft.DoesNotExist:
            return Response({'error': 'NFT не найдена'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Удаление NFT по id",
        responses={204: 'success', 404: 'NFT не найдена'}
    )
    def delete(self, request, pk):
        try:
            nft = Nft.objects.get(pk=pk)
        except Nft.DoesNotExist:
            return Response({'error': 'NFT не найдена'}, status=status.HTTP_404_NOT_FOUND)
        nft.delete()
        return Response("success", status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Обновление информации об NFT по id",
        request_body=NftSerializer,
        responses={200: NftSerializer, 400: 'Bad Request', 404: 'NFT не найдена'}
    )
    def put(self, request, pk):
        try:
            nft = Nft.objects.get(pk=pk)
        except Nft.DoesNotExist:
            return Response({'error': 'NFT не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = NftSerializer(nft, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(APIView):
    @swagger_auto_schema(
        operation_description="Получение всех категорий",
        responses={200: CatSerializer(many=True)}
    )
    def get(self, request):
        cat = Category.objects.all()
        serializer = CatSerializer(cat, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Создание новой категории",
        request_body=CatSerializer,
        responses={201: CatSerializer}
    )
    def post(self, request):
        serializer = CatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Получение категории по id",
        responses={200: CatSerializer, 404: 'Категория не найдена'}
    )
    def get(self, request, pk):
        try:
            cat = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CatSerializer(cat)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Обновление информации о категории по id",
        request_body=CatSerializer,
        responses={200: CatSerializer, 400: 'Bad Request', 404: 'Категория не найдена'}
    )
    def put(self, request, pk):
        try:
            cat = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CatSerializer(cat, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Удаление категории по id",
        responses={204: 'success', 404: 'Категория не найдена'}
    )
    def delete(self, request, pk):
        try:
            cat = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
        cat.delete()
        return Response("success", status=status.HTTP_204_NO_CONTENT)



