from rest_framework.serializers import ModelSerializer
from store.models import Nft, Category, TypePrice


class CatSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NftSerializer(ModelSerializer):
    class Meta:
        model = Nft
        fields = '__all__'


class TypePriceSerializer(ModelSerializer):
    class Meta:
        modul = TypePrice
        fields = '__all__'
