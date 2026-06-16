import paypalrestsdk
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from courses.models import Course, Enrollment
from .models import Payment


def get_paypal_api():
    return paypalrestsdk.Api({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })


@login_required
def create_payment(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course.")
        return redirect("course_detail", slug=course.slug)

    amount = str(course.effective_price)
    api = get_paypal_api()

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(
                reverse("payment_execute", args=[course.slug])
            ),
            "cancel_url": request.build_absolute_uri(
                reverse("payment_cancel", args=[course.slug])
            ),
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": course.title,
                    "sku": str(course.id),
                    "price": amount,
                    "currency": "USD",
                    "quantity": 1,
                }]
            },
            "amount": {
                "total": amount,
                "currency": "USD",
            },
            "description": f"Enrollment in: {course.title}",
        }],
    }, api=api)

    if payment.create():
        Payment.objects.create(
            user=request.user,
            course=course,
            paypal_payment_id=payment.id,
            amount=course.effective_price,
            status="created",
        )
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)

    messages.error(request, "Something went wrong with PayPal. Please try again.")
    return redirect("course_detail", slug=course.slug)


@login_required
def execute_payment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    if not payment_id or not payer_id:
        messages.error(request, "Invalid payment details.")
        return redirect("course_detail", slug=course.slug)

    api = get_paypal_api()
    payment = paypalrestsdk.Payment.find(payment_id, api=api)

    if payment.execute({"payer_id": payer_id}):
        db_payment = Payment.objects.filter(paypal_payment_id=payment_id).first()
        if db_payment:
            db_payment.status = "approved"
            db_payment.save()

        Enrollment.objects.get_or_create(user=request.user, course=course)
        messages.success(request, f"Payment successful! You are now enrolled in {course.title}.")
        return redirect("payment_success", slug=course.slug)

    messages.error(request, "Payment could not be completed.")
    return redirect("course_detail", slug=course.slug)


@login_required
def payment_cancel(request, slug):
    course = get_object_or_404(Course, slug=slug)
    messages.warning(request, "Payment was cancelled.")
    return redirect("course_detail", slug=course.slug)


@login_required
def payment_success(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "payments/success.html", {"course": course})
