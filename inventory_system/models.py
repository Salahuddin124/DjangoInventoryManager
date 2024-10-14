# models.py

from django.db import models
from datetime import date
from django.core.validators import MinValueValidator

class Products(models.Model):
    COMPUTING_EQUIPMENT = "Computing Equipment"
    AUDIO_VISUAL_EQUIPMENT = "Audio-Visual Equipment"
    LABORATORY_EQUIPMENT = "Laboratory Equipment"
    WORKSHOP_TOOLS = "Workshop Tools"
    OFFICE_EQUIPMENT = "Office Equipment"
    EDUCATIONAL_TEACHING_AIDS = "Educational and Teaching Aids"
    MISCELLANEOUS = "Miscellaneous"
    categories = [
        (COMPUTING_EQUIPMENT, "Computing Equipment"),
        (AUDIO_VISUAL_EQUIPMENT, "Audio-Visual Equipment"),
        (LABORATORY_EQUIPMENT, "Laboratory Equipment"),
        (WORKSHOP_TOOLS, "Workshop Tools"),
        (OFFICE_EQUIPMENT, "Office Equipment"),
        (EDUCATIONAL_TEACHING_AIDS, "Educational and Teaching Aids"),
        (MISCELLANEOUS, "Miscellaneous"),
    ]
  
    name = models.CharField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])  # Ensure quantity is always >= 1
    category = models.CharField(max_length=200, choices=categories, default=COMPUTING_EQUIPMENT)
    image = models.ImageField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    availability = models.BooleanField(default=True, null=False)
  
    def __str__(self):
        return self.name
  
    @property
    def image_url(self):
        try:
            url = self.image.url
        except ValueError:
            url = ""
        return url  # Corrected return statement to return the actual URL

class Reservation(models.Model):
    PENDING = 'Pending'

    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    quantity = models.IntegerField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    product_name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)  
    status = models.CharField(max_length=50, default=PENDING)

    def __str__(self):
        return f"Reservation for {self.quantity} {self.product.name} by {self.username}"
