from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "amount", "status", "paypal_payment_id", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["paypal_payment_id", "user__username"]
    readonly_fields = ["paypal_payment_id", "amount", "currency", "status"]
