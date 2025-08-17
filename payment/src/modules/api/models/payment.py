from django.db import models


class PaymentStatus(models.TextChoices):
    PENDING = "Pending"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    CANCELED = "Canceled"


class PaymentMethod(models.TextChoices):
    CREDIT_CARD = "Credit Card"
    PAYPAL = "PayPal"
    SBER_PAY = "Sber Pay"


class PaymentCurrency(models.TextChoices):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


class PaymentManager(models.Manager):
    def create(self, user_id, amount, currency, payment_method):
        payment = Payment(
            user_id=user_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.COMPLETED,
            payment_method=payment_method,
        )
        payment.save()
        return payment


class Payment(models.Model):
    user_id = models.IntegerField(verbose_name="User ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=PaymentCurrency.choices)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PaymentManager()
