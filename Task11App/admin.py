from django.contrib import admin
from .models import *


class BuildingAdmin(admin.ModelAdmin):
    pass


class ContractAdmin(admin.ModelAdmin):
    pass


class ContractBuildingConnectionAdmin(admin.ModelAdmin):
    pass


class FixedAssetAdmin(admin.ModelAdmin):
    pass


class ServiceAdmin(admin.ModelAdmin):
    pass


class InvoiceForPaymentAdmin(admin.ModelAdmin):
    pass


class DistributedInvoiceForPaymentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Building, BuildingAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractBuildingConnection, ContractBuildingConnectionAdmin)
admin.site.register(FixedAsset, FixedAssetAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(InvoiceForPayment, InvoiceForPaymentAdmin)
admin.site.register(DistributedInvoiceForPayment, DistributedInvoiceForPaymentAdmin)