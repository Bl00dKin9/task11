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


class_lookup = {'building': Building, 'contract': Contract, 'contract_building_connection': ContractBuildingConnection, 'fixed_asset': FixedAsset,
                        'service': Service, 'invoice_for_payment': InvoiceForPayment, 'distributed_invoice_for_payment': DistributedInvoiceForPayment}


serializer_class_lookup = {'building': BuildingSerializer, 'contract': ContractSerializer, 'contract_building_connection': ContractBuildingConnectionSerializer,
                           'fixed_asset': FixedAssetSerializer, 'service': ServiceSerializer, 'invoice_for_payment': InvoiceForPaymentSerializer,
                           'distributed_invoice_for_payment': DistributedInvoiceForPaymentSerializer}


def upload_building_file(worksheet):
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


def upload_contract_file(worksheet):
    contracts = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            contract = Contract(contract_id=row[0].value, contract_beginning_date=row[1].value, contract_ending_date=row[2].value)
            contracts.append(contract)
        Contract.objects.bulk_create(contracts)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_contract_building_connection_file(worksheet):
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


def upload_fixed_asset_file(worksheet):
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


def upload_service_file(worksheet):
    services = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            service = Service(service_id=row[0].value, service_class=row[1].value)
            services.append(service)
        Service.objects.bulk_create(services)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_invoice_for_payment_file(worksheet):
    invoice_for_payments = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            invoice_for_payment = InvoiceForPayment(company=row[0].value, year=row[1].value, invoice_number=row[2].value, invoice_position=row[3].value, service_id=row[4].value,
                                                    contract_id=row[5].value, invoice_reflection_in_the_accounting_system_date=row[6].value, cost_excluding_VAT=row[7].value)
            invoice_for_payments.append(invoice_for_payment)
        InvoiceForPayment.objects.bulk_create(invoice_for_payments)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def upload_distributed_invoice_for_payment_file(worksheet):
    distributed_invoice_for_payments = []
    try:
        for row in worksheet.iter_rows(min_row=2):
            distributed_invoice_for_payment = DistributedInvoiceForPayment(company=row[0].value, year=row[1].value, invoice_number=row[2].value, invoice_position=row[3].value,
                                                                           distribution_position_number=row[4].value, reflection_in_the_accounting_system_date=row[5].value,
                                                                           contract_id=row[6].value, service_id=row[7].value, service_class=row[8].value, building_id=row[9].value,
                                                                           fixed_asset_class=row[10].value, fixed_asset_id=row[11].value, is_used_in_main_activity=(row[12].value == 'X'),
                                                                           is_used_in_rent=(row[13].value == 'X'), square=row[14].value, distribution_sum=row[15].value,
                                                                           general_ledger_account=row[16].value)
            distributed_invoice_for_payments.append(distributed_invoice_for_payment)
        DistributedInvoiceForPayment.objects.bulk_create(distributed_invoice_for_payments)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


@api_view(['POST'])
def upload_file(request, table_name):
    excel_file = request.FILES["excel_file"]
    wb = openpyxl.load_workbook(excel_file)
    worksheet = wb["Sheet1"]
    response = globals()['upload_' + table_name + '_file'](worksheet)
    return response


@api_view(['POST'])
def upload_json(request, table_name):
    serializer = serializer_class_lookup[table_name](data=request.data, many=True)
    if serializer.is_valid():
        id_list = []
        res = serializer.save()
        for i in range(len(res)):
            id_list.append(res[i].id)
        return start_distribution(id_list)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def start_distribution(id_list):
    try:
        for i in range(len(id_list)):
            distributed_invoice_for_payments = []
            count = 1
            square_sum = 0
            invoice_for_payment = InvoiceForPayment.objects.get(pk=id_list[i])
            company = invoice_for_payment.company
            year = invoice_for_payment.year
            invoice_number = invoice_for_payment.invoice_number
            invoice_position = invoice_for_payment.invoice_position
            service_id = invoice_for_payment.service_id
            services = Service.objects.filter(service_id=service_id)
            service_class = services[0].service_class
            reflection_in_the_accounting_system_date = invoice_for_payment.invoice_reflection_in_the_accounting_system_date
            cost_excluding_VAT = invoice_for_payment.cost_excluding_VAT
            contract_id = invoice_for_payment.contract_id
            contract_building_connections = ContractBuildingConnection.objects.filter(contract_id=contract_id)
            for j in range(len(contract_building_connections)):
                building_id = contract_building_connections[j].building_id
                fixed_assets = FixedAsset.objects.filter(building_id=building_id)
                for k in range(len(fixed_assets)):
                    fixed_asset_id = fixed_assets[k].fixed_asset_id
                    fixed_asset_class = fixed_assets[k].fixed_asset_class
                    is_used_in_main_activity = fixed_assets[k].is_used_in_main_activity
                    is_used_in_rent = fixed_assets[k].is_used_in_rent
                    square = fixed_assets[k].square
                    distributed_invoice_for_payment = DistributedInvoiceForPayment(company=company, year=year, invoice_number=invoice_number, invoice_position=invoice_position,
                                                                                   distribution_position_number=count,
                                                                                   reflection_in_the_accounting_system_date=reflection_in_the_accounting_system_date,
                                                                                   contract_id=contract_id, service_id=service_id, service_class=service_class, building_id=building_id,
                                                                                   fixed_asset_class=fixed_asset_class, fixed_asset_id=fixed_asset_id,
                                                                                   is_used_in_main_activity=is_used_in_main_activity, is_used_in_rent=is_used_in_rent,
                                                                                   square=square, distribution_sum=0)
                    distributed_invoice_for_payments.append(distributed_invoice_for_payment)
                    count += 1
                    square_sum += square
            for j in range(len(distributed_invoice_for_payments)):
                distributed_invoice_for_payments[j].distribution_sum = cost_excluding_VAT * distributed_invoice_for_payments[j].square / square_sum
            DistributedInvoiceForPayment.objects.bulk_create(distributed_invoice_for_payments)
    except Exception as err:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return HttpResponse(status=200)


def index(request):
    selected_object = str(request.POST.get('selected_object'))
    if selected_object == "None":
        selected_object = 'building'
    if 'delete' in request.POST:
        class_lookup[selected_object].objects.all().delete()
    return render(request, 'index.html', {"object": selected_object})