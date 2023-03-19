from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import PortManager


class BaseRate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name="Rate price"
    )
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.price} {self.valid_from} - {self.valid_until}"


class CarrierIds(models.TextChoices):
    COSU = "COSU", _("COSCO")
    MSCU = "MSCU", _("Mediterranean Shipping Company")
    HLCU = "HLCU", _("Hapag-Lloyd")
    MAEU = "MAEU", _("Maersk")


class ContainerTypes(models.TextChoices):
    TWENTY_FOOTER = "22GP", _("20 foot container")
    FOURTY_FOOTER = "42GP", _("Standart 40 foot container")
    FOURTY_FOOTER_HC = "45GP", _("40 foot high cube container")


class Port(models.Model):
    country_code = models.CharField(max_length=10)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)

    objects = PortManager()

    def __str__(self):
        return f"{self.name} ({self.code})"


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name


class MainRate(BaseRate):
    carrier_id = models.CharField(max_length=10, choices=CarrierIds.choices)
    container_type = models.CharField(max_length=10, choices=ContainerTypes.choices)
    pol = models.ForeignKey(Port, on_delete=models.CASCADE, related_name="pol")
    pod = models.ForeignKey(Port, on_delete=models.CASCADE, related_name="pod")

    def __str__(self) -> str:
        return f"{self.pol} {self.pod} {self.carrier_id} {self.container_type}"


class SurchargeTypes(models.TextChoices):
    DANGEROUS_GOODS = "danger", _("Surcharge for Dangerous Goods")
    CUSTOMS_FEE = "customs", _("Surcharge for Customs Fee")


class Surcharge(BaseRate):
    carrier_id = models.CharField(max_length=10, choices=CarrierIds.choices)
    surcharge_type = models.CharField(max_length=10, choices=SurchargeTypes.choices)

    def __str__(self) -> str:
        return f" {self.carrier_id}" + super().__str__()
