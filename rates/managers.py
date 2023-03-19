# create a manager for Port model in rates app

# app/rates/managers.py
from typing import Dict, List
from django.db import models
from django.db.models import Q


class PortManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
        )

    def filter_by_params(
        self, code: str = None, name: str = None, country_code: str = None
    ):
        query = Q()
        if code:
            query |= Q(code=code)
        if name:
            query |= Q(name=name)
        if country_code:
            query |= Q(country_code=country_code)

        return self.filter(query)
