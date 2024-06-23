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


class DistributedInvoiceForPaymentWithoutIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributedInvoiceForPayment
        fields = ('company', 'year', 'invoice_number', 'invoice_position', 'distribution_position_number', 'reflection_in_the_accounting_system_date', 'contract_id', 'service_id',
                  'service_class', 'building_id', 'fixed_asset_class', 'fixed_asset_id', 'is_used_in_main_activity', 'is_used_in_rent', 'square', 'distribution_sum', 'general_ledger_account')

