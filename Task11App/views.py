from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *
import openpyxl
from http import HTTPStatus
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden)
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

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


def upload_building_file(row, user):
    return Building.objects.create(building_id=row[0], possession_beginning_date=row[1], possession_ending_date=row[2], measurement_ending_date=row[3],
                                   measurement_beginning_date=row[4], square=row[5], measure_unit=row[6])


def upload_contract_file(row, user):
    return Contract.objects.create(contract_id=row[0], contract_beginning_date=row[1], contract_ending_date=row[2])


def upload_contract_building_connection_file(row, user):
    return ContractBuildingConnection.objects.create(contract_id=row[0], building_id=row[1], connection_beginning_date=row[2], connection_ending_date=row[3])


def upload_fixed_asset_file(row, user):
    return FixedAsset.objects.create(fixed_asset_id=row[0], fixed_asset_class=row[1], is_used_in_main_activity=(row[2] == 'X'), is_used_in_rent=(row[3] == 'X'), square=row[4],
                                     measure_unit=row[5], building_id=row[6], connection_with_building_beginning_date=row[7], connection_with_building_ending_date=row[8],
                                     place_in_service_date=row[9], disposal_date=row[10])


def upload_service_file(row, user):
    return Service.objects.create(service_id=row[0], service_class=row[1])


def upload_invoice_for_payment_file(row, user):
    return InvoiceForPayment.objects.create(company=row[0], year=row[1], invoice_number=row[2], invoice_position=row[3], service_id=row[4],
                                            contract_id=row[5], invoice_reflection_in_the_accounting_system_date=row[6], cost_excluding_VAT=row[7], user=user)


def upload_distributed_invoice_for_payment_file(row, user):
    return DistributedInvoiceForPayment.objects.create(company=row[0], year=row[1], invoice_number=row[2], invoice_position=row[3], distribution_position_number=row[4],
                                                       reflection_in_the_accounting_system_date=row[5], contract_id=row[6], service_id=row[7], service_class=row[8],
                                                       building_id=row[9], fixed_asset_class=row[10], fixed_asset_id=row[11], is_used_in_main_activity=(row[12] == 'X'),
                                                       is_used_in_rent=(row[13] == 'X'), square=row[14], distribution_sum=row[15], general_ledger_account=row[16], user=user)


@api_view(['POST'])
def upload_file(request, table_name):
    user = None
    if table_name == "invoice_for_payment" or table_name == "distributed_invoice_for_payment":
        try:
            username = request.data['username']
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    excel_file = request.FILES["excel_file"]
    wb = openpyxl.load_workbook(excel_file)
    worksheet = wb["Sheet1"]
    for row in worksheet.iter_rows():
        try:
            if globals()['upload_' + table_name + '_file'](row, user) is not None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return HttpResponse(status=200)