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


def upload_building_file(worksheet, user):
    buildings = []
    try:
        for row in worksheet.iter_rows(min_row=2):
                building = Building(building_id=row[0].value, possession_beginning_date=row[1].value, possession_ending_date=row[2].value, measurement_ending_date=row[3].value,
                                    measurement_beginning_date=row[4].value, square=row[5].value, measure_unit=row[6].value)
                buildings.append(building)
        Building.objects.bulk_create(buildings)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_contract_file(worksheet, user):
    contracts = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            contract = Contract(contract_id=row[0].value, contract_beginning_date=row[1].value, contract_ending_date=row[2].value)
            contracts.append(contract)
        Contract.objects.bulk_create(contracts)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_contract_building_connection_file(worksheet, user):
    contract_building_connections = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            contract_building_connection = ContractBuildingConnection(contract_id=row[0].value, building_id=row[1].value, connection_beginning_date=row[2].value,
                                                                      connection_ending_date=row[3].value)
            contract_building_connections.append(contract_building_connection)
        ContractBuildingConnection.objects.bulk_create(contract_building_connections)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_fixed_asset_file(worksheet, user):
    fixed_assets = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            fixed_asset = FixedAsset(fixed_asset_id=row[0].value, fixed_asset_class=row[1].value, is_used_in_main_activity=(row[2].value == 'X'),
                                     is_used_in_rent=(row[3].value == 'X'), square=row[4].value, measure_unit=row[5].value, building_id=row[6].value,
                                     connection_with_building_beginning_date=row[7].value, connection_with_building_ending_date=row[8].value, place_in_service_date=row[9].value,
                                     disposal_date=row[10].value)
            fixed_assets.append(fixed_asset)
        FixedAsset.objects.bulk_create(fixed_assets)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_service_file(worksheet, user):
    services = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            service = Service(service_id=row[0].value, service_class=row[1].value)
            services.append(service)
        Service.objects.bulk_create(services)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_invoice_for_payment_file(worksheet, user):
    invoice_for_payments = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            invoice_for_payment = InvoiceForPayment(company=row[0].value, year=row[1].value, invoice_number=row[2].value, invoice_position=row[3].value, service_id=row[4].value,
                                                    contract_id=row[5].value, invoice_reflection_in_the_accounting_system_date=row[6].value, cost_excluding_VAT=row[7].value, user=user)
            invoice_for_payments.append(invoice_for_payment)
        InvoiceForPayment.objects.bulk_create(invoice_for_payments)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_distributed_invoice_for_payment_file(worksheet, user):
    distributed_invoice_for_payments = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            distributed_invoice_for_payment = DistributedInvoiceForPayment(company=row[0].value, year=row[1].value, invoice_number=row[2].value, invoice_position=row[3].value,
                                                                           distribution_position_number=row[4].value, reflection_in_the_accounting_system_date=row[5].value,
                                                                           contract_id=row[6].value, service_id=row[7].value, service_class=row[8].value, building_id=row[9].value,
                                                                           fixed_asset_class=row[10].value, fixed_asset_id=row[11].value, is_used_in_main_activity=(row[12].value == 'X'),
                                                                           is_used_in_rent=(row[13].value == 'X'), square=row[14].value, distribution_sum=row[15].value,
                                                                           general_ledger_account=row[16].value, user=user)
            distributed_invoice_for_payments.append(distributed_invoice_for_payment)
        DistributedInvoiceForPayment.objects.bulk_create(distributed_invoice_for_payments)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


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
    response = globals()['upload_' + table_name + '_file'](worksheet, user)

    return response


def index(request):
    selected_object = str(request.POST.get('selected_object'))
    if selected_object == "None":
        selected_object = 'building'
    if 'delete' in request.POST:
        class_lookup = {'building': Building, 'contract': Contract, 'contract_building_connection': ContractBuildingConnection, 'fixed_asset': FixedAsset,
                        'service': Service, 'invoice_for_payment': InvoiceForPayment, 'distributed_invoice_for_payment': DistributedInvoiceForPayment}
        class_lookup[selected_object].objects.all().delete()
    return render(request, 'index.html', {"object": selected_object})