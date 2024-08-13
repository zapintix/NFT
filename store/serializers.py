from rest_framework import serializers
from store.models import Nft, Category, TypePrice


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NftSerializer(serializers.ModelSerializer):
    cat = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Category.objects.all())
    typePrice = serializers.PrimaryKeyRelatedField(read_only=False, queryset=TypePrice.objects.all())

    class Meta:
        model = Nft
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['cat'] = instance.cat.name
        ret['typePrice'] = instance.typePrice.name
        return ret


class TypePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePrice
        fields = '__all__'
