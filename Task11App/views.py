from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import *
from .serializers import *


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractBuildingConnectionViewSet(viewsets.ModelViewSet):
    queryset = ContractBuildingConnection.objects.all()
    serializer_class = ContractBuildingConnectionSerializer


class FixedAssetViewSet(viewsets.ModelViewSet):
    queryset = FixedAsset.objects.all()
    serializer_class = FixedAssetSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class InvoiceForPaymentViewSet(viewsets.ModelViewSet):
    queryset = InvoiceForPayment.objects.all()
    serializer_class = InvoiceForPaymentSerializer


class DistributedInvoiceForPaymentViewSet(viewsets.ModelViewSet):
    queryset = DistributedInvoiceForPayment.objects.all()
    serializer_class = DistributedInvoiceForPaymentSerializer