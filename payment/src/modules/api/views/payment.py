import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from ..models import Payment

from utils import Logger

log = Logger.get_instance()


class PaymentAPIView(APIView):
    @extend_schema(
        responses={
            status.HTTP_201_CREATED: {"description": "Payment created successfully"},
            status.HTTP_400_BAD_REQUEST: {"description": "Payment info is not provided"},
        }
    )
    def post(self, request):
        """
        Handle POST requests to create a new payment.
        """
        payment_info = request.data
        log.debug(f"Received payment info: {payment_info}")
        if not payment_info:
            return Response(
                {"error": "Payment info is not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Simulate processing time
        time.sleep(1)
        payment = Payment.objects.create(**payment_info)
        payment.save()
        log.debug(f"Payment created: {payment.id}")

        return Response(
            {
                "message": "Payment created successfully",
                "payment_id": payment.id,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: {"description": "Payment created successfully"},
            status.HTTP_404_NOT_FOUND: {"description": "Payment not found"},
        }
    )
    def get(self, request):
        """
        Handle GET requests to retrieve payment information.
        """
        payment_id = request.query_params.get("payment_id", None)
        if not payment_id:
            return Response(
                json={"error": "Payment ID not provided"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            payment = Payment.objects.get(id=payment_id)
            return Response(json={"payment": payment.to_dict()}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response(
                json={"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )
