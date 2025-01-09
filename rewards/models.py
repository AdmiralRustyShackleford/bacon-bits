from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class QRCode(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='qr_codes')
    unique_code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.unique_code

class Survey(models.Model):
    qr_code = models.OneToOneField('QRCode', on_delete=models.CASCADE, related_name='survey')
    question = models.TextField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Survey for QR Code {self.qr_code.unique_code}"
    
class PointTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_transactions')
    points = models.IntegerField()
    reason = models.CharField(max_length=255) # e.g., "Survey Completion", "Product Repemption"
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.points} points awarded for {self.reason}"