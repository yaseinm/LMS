from django.db import models
from django.conf import settings
from courses.models import Course


class Payment(models.Model):
    STATUS_CHOICES = [
        ("created", "Created"),
        ("approved", "Approved"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="payments"
    )
    paypal_payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.paypal_payment_id} - {self.status}"
