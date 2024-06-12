from rest_framework import serializers
from .models import *


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class ContractBuildingConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractBuildingConnection
        fields = '__all__'


class FixedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedAsset
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class InvoiceForPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceForPayment
        fields = '__all__'


class DistributedInvoiceForPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributedInvoiceForPayment
        fields = '__all__'
