from rest_framework import serializers
from commons.models.dummy import DummyItem

class DummyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyItem
        fields = '__all__'