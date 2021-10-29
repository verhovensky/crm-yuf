from django import forms
from decimal import Decimal
# for custom encoder
from datetime import datetime, date
from time import time, struct_time, mktime
import json
# min value validator for minus quantity check
from django.core.validators import MinValueValidator


# decimal decode

# import json
# from django.core.serializers.json import DjangoJSONEncoder
# from django.forms.models import model_to_dict
#
# model_instance = YourModel.object.first()
# model_dict = model_to_dict(model_instance)
#
# json.dumps(model_dict, cls=DjangoJSONEncoder)

# PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)
        if isinstance(o, date):
            return str(o)
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, struct_time):
            return datetime.fromtimestamp(mktime(o))
        # Any other serializer if needed
        return super(CustomJSONEncoder, self).default(o)


class CartAddProductForm(forms.Form):
    quantity = forms.DecimalField(min_value=1.0, max_digits=10,
                                  validators=[MinValueValidator(Decimal('1.0'))], label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

