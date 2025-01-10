import qrcode
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
    content = models.TextField(help_text="The data encoded in the QR code (e.g., URL or unique identifier).",
                               default="default_content")
    image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate the QR code image before saving
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.content)
        qr.make(fit=True)
        
        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white") # make it look like bacon later
        
        # Save the image to the ImageField
        from io import BytesIO
        from django.core.files.base import ContentFile
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.image.save(f"qr_code_{self.id}.png", ContentFile(buffer.getvalue()), save=False)
        
        super().save(*args, **kwargs)
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