from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *


router = DefaultRouter()
router.register('api/building', BuildingViewSet)
router.register('api/contract', ContractViewSet)
router.register('api/contract_building_connection', ContractBuildingConnectionViewSet)
router.register('api/fixed_asset', FixedAssetViewSet)
router.register('api/service', ServiceViewSet)
router.register('api/invoice_for_payment', InvoiceForPaymentViewSet)
router.register('api/distributed_invoice_for_payment', DistributedInvoiceForPaymentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('index', views.index),
    path('api/<str:table_name>/upload_excel', views.upload_file),
    path('api/<str:table_name>/upload_json', views.upload_json),
]