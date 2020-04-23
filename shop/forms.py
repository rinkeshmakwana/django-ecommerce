from django import forms


PAYMENT_CHOICES = (
    ('C', 'Card'),
    ('P', 'PayPal'),
)


class CheckoutForm(forms.Form):
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    country = forms.CharField(required=False)
    zip = forms.CharField(required=False)

    use_default_address = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
