from django.contrib import admin

# Register all models from app.rates.models
from rates.models import (
    Category,
    MainRate,
    Port,
    Surcharge,
)

admin.site.register(Category)
admin.site.register(MainRate)
admin.site.register(Port)
admin.site.register(Surcharge)
