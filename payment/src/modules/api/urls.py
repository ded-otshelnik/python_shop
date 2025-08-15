from django.urls import path
from rest_framework import routers
from .views import PaymentAPIView

router = routers.DefaultRouter()
router.register(r"payment", PaymentAPIView, basename="payment")

urlpatterns = [
    path("payment/", PaymentAPIView.as_view(), name="payment"),
]
