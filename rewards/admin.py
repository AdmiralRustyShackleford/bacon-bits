from django.contrib import admin
from .models import Product, QRCode, Survey, PointTransaction

admin.site.register(Product)
admin.site.register(QRCode)
admin.site.register(Survey)
admin.site.register(PointTransaction)
