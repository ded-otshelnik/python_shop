from django import forms


class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=[
            ("credit_card", "Credit Card"),
            ("paypal", "PayPal"),
            ("sber_pay", "Sber Pay"),
        ]
    )
    shipping_method = forms.ChoiceField(
        choices=[
            ("standard", "Standard Shipping"),
            ("express", "Express Shipping"),
        ]
    )

    def clean_data(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")
        shipping_method = cleaned_data.get("shipping_method")
        if not payment_method:
            self.add_error("payment_method", "Payment method is required.")

        if not shipping_method:
            self.add_error("shipping_method", "Shipping method is required.")

        return cleaned_data
