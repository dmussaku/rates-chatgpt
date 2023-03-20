import itertools

from django.core.management.base import BaseCommand
from django.db import transaction

from rates.factories import MainRateFactory, SurchargeFactory, PortFactory
from rates.models import (
    MainRate,
    Surcharge,
    Port,
    CarrierIds,
    ContainerTypes,
    SurchargeTypes,
)


class Command(BaseCommand):
    help = "Create test data for rates app"

    def generate_ports(self):
        # create 10 ports which are the most popular
        PortFactory.create(
            **{"code": "CNSHA", "country_code": "CN", "name": "Shanghai Port"}
        )
        PortFactory.create(
            **{"code": "SGSIN", "country_code": "SG", "name": "Port of Singapore"}
        )
        PortFactory.create(
            **{"code": "CNNGB", "country_code": "CN", "name": "Port of Ningbo-Zhoushan"}
        )
        PortFactory.create(
            **{"code": "KRPUS", "country_code": "KR", "name": "Port of Busan"}
        )
        PortFactory.create(
            **{"code": "CNGZU", "country_code": "CN", "name": "Port of Guangzhou"}
        )
        PortFactory.create(
            **{"code": "NLRTM", "country_code": "NL", "name": "Port of Rotterdam"}
        )
        PortFactory.create(
            **{"code": "CNTAO", "country_code": "CN", "name": "Port of Qingdao"}
        )
        PortFactory.create(
            **{"code": "CNTSN", "country_code": "CN", "name": "Port of Tianjin"}
        )
        PortFactory.create(
            **{"code": "AEJEA", "country_code": "AE", "name": "Port of Jebel Ali"}
        )
        PortFactory.create(
            **{"code": "USLAX", "country_code": "US", "name": "Port of Los Angeles"}
        )
        PortFactory.create(
            **{"code": "CNDLC", "country_code": "CN", "name": "Port of Dalian"}
        )
        PortFactory.create(
            **{"code": "DEHAM", "country_code": "DE", "name": "Port of Hamburg"}
        )
        PortFactory.create(
            **{"code": "MYPKG", "country_code": "MY", "name": "Port Klang"}
        )
        PortFactory.create(
            **{
                "code": "USNYC",
                "country_code": "US",
                "name": "Port of New York and New )Jersey",
            }
        )
        PortFactory.create(
            **{"code": "JPYOK", "country_code": "JP", "name": "Port of Yokohama"}
        )
        PortFactory.create(
            **{"code": "CNXMN", "country_code": "CN", "name": "Port of Xiamen"}
        )
        PortFactory.create(
            **{"code": "DEBRV", "country_code": "DE", "name": "Port of Bremerhaven"}
        )
        PortFactory.create(
            **{"code": "TWKHH", "country_code": "TW", "name": "Port of Kaohsiung"}
        )
        PortFactory.create(
            **{"code": "ESVLC", "country_code": "ES", "name": "Port of Valencia"}
        )
        PortFactory.create(
            **{"code": "CNLYG", "country_code": "CN", "name": "Port of Lianyungang"}
        )

        print("Created ports: ", Port.objects.count())

    def generate_main_rates(self):
        with transaction.atomic():
            for container_type, carrier_id in itertools.product(
                [choice for choice, label in ContainerTypes.choices],
                [choice for choice, label in CarrierIds.choices],
            ):
                for pol, pod in itertools.combinations(Port.objects.all(), 2):
                    MainRateFactory.create(
                        carrier_id=carrier_id,
                        container_type=container_type,
                        pol=pol,
                        pod=pod,
                    )
        print("Created main rates: ", MainRate.objects.count())

    def generate_surcharges(self):
        # generate surcharges for every container type and carrier
        for surcharge_type, carrier_id in itertools.product(
            [choice for choice, label in SurchargeTypes.choices],
            [choice for choice, label in CarrierIds.choices],
        ):
            SurchargeFactory.create(
                carrier_id=carrier_id,
                surcharge_type=surcharge_type,
            )
        print("Created surcharges: ", Surcharge.objects.count())

    def handle(self, *args, **options):
        with transaction.atomic():
            self.generate_ports()
            self.generate_main_rates()
            self.generate_surcharges()

        self.stdout.write(self.style.SUCCESS("Successfully created test data"))
