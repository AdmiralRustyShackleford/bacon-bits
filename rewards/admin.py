from django.contrib import admin
from .models import Product, QRCode, Survey, PointTransaction

admin.site.register(Product)
admin.site.register(Survey)
admin.site.register(PointTransaction)

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at')