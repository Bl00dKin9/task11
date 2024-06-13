from django.db import models
from  django.contrib.auth.models import User


# Create your models here.
class Building(models.Model):
    building_id = models.CharField(verbose_name="Здание")
    possession_beginning_date = models.DateField(verbose_name="Начало владения")
    possession_ending_date = models.DateField(verbose_name="Конец владения")
    measurement_ending_date = models.DateField(verbose_name="Конец действия измерения")
    measurement_beginning_date = models.DateField(verbose_name="Начало действия измерения", null=True)
    square = models.DecimalField(verbose_name="Площадь", max_digits=10, decimal_places=3)
    measure_unit = models.CharField(verbose_name="Единица измерения")


class Contract(models.Model):
    contract_id = models.CharField(verbose_name="ID договора")
    contract_beginning_date = models.DateField(verbose_name="Начало действия договора")
    contract_ending_date = models.DateField(verbose_name="Конец действия договора")


class ContractBuildingConnection(models.Model):
    contract_id = models.CharField(verbose_name="ID договора")
    building_id = models.CharField(verbose_name="ID здания")
    connection_beginning_date = models.DateField(verbose_name="Начало действия отношения")
    connection_ending_date = models.DateField(verbose_name="Конец действия отношения")


class FixedAsset(models.Model):
    fixed_asset_id = models.CharField(verbose_name="ID основного средства")
    fixed_asset_class = models.CharField(verbose_name="Класс основного средства")
    is_used_in_main_activity = models.BooleanField(verbose_name="Признак \"Используется в основной деятельности\"")
    is_used_in_rent = models.BooleanField(verbose_name="Признак \"Способ использования\"")
    square = models.DecimalField(verbose_name="Площадь", max_digits=10, decimal_places=3, null=True)
    measure_unit = models.CharField(verbose_name="Единица измерения", null=True)
    building_id = models.CharField(verbose_name="ID здания", null=True)
    connection_with_building_beginning_date = models.DateField(verbose_name="Начало действия связи со зданием")
    connection_with_building_ending_date = models.DateField(verbose_name="Конец действия связи со зданием")
    place_in_service_date = models.DateField(verbose_name="Дата ввода в эксплуатацию")
    disposal_date = models.DateField(verbose_name="Дата выбытия", null=True, blank=True)


class Service(models.Model):
    service_id = models.CharField(verbose_name="ID услуги")
    service_class = models.CharField(verbose_name="Класс услуги")


class InvoiceForPayment(models.Model):
    company = models.CharField(verbose_name="Компания")
    year = models.IntegerField(verbose_name="Год")
    invoice_number = models.CharField(verbose_name="Номер счета")
    invoice_position = models.IntegerField(verbose_name="Позиция счета")
    service_id = models.CharField(verbose_name="ID услуги")
    contract_id = models.CharField(verbose_name="ID договора")
    invoice_reflection_in_the_accounting_system_date = models.DateField(verbose_name="Дата отражения счета в учетной системе", null=True)
    cost_excluding_VAT = models.DecimalField(verbose_name="Стоимость без НДС", max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'invoice_number', 'invoice_position'], name='unique_year_invoice_number_invoice_position_combination'
            )
        ]


class DistributedInvoiceForPayment(models.Model):
    company = models.CharField(verbose_name="Компания")
    year = models.IntegerField(verbose_name="Год")
    invoice_number = models.CharField(verbose_name="Номер счета")
    invoice_position = models.IntegerField(verbose_name="Позиция счета")
    distribution_position_number = models.IntegerField(verbose_name="Номер позиции распределения")
    reflection_in_the_accounting_system_date = models.DateField(verbose_name="Дата отражения в учетной системе", null=True)
    contract_id = models.CharField(verbose_name="ID договора")
    service_id = models.CharField(verbose_name="ID услуги")
    service_class = models.CharField(verbose_name="Класс услуги")
    building_id = models.CharField(verbose_name="Здание", null=True)
    fixed_asset_class = models.CharField(verbose_name="Класс основного средства", null=True)
    fixed_asset_id = models.CharField(verbose_name="ID основного средства")
    is_used_in_main_activity = models.BooleanField(verbose_name="Признак \"Используется в основной деятельности\"")
    is_used_in_rent = models.BooleanField(verbose_name="Признак \"Способ использования\"")
    square = models.DecimalField(verbose_name="Площадь", max_digits=10, decimal_places=3)
    distribution_sum = models.DecimalField(verbose_name="Сумма распределения", max_digits=10, decimal_places=2)
    general_ledger_account = models.CharField(verbose_name="Счет главной книги", null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'invoice_number', 'invoice_position', 'distribution_position_number'], name='unique_year_invoice_number_invoice_position_distribution_position_number_combination'
            )
        ]