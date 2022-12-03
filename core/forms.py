import re

from django import forms
from django.core.exceptions import ValidationError

from core.models import Product


class SearchProductForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100'}),
        required=False
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'quantity', 'price', 'available')

    name = forms.CharField(
        error_messages={'required': 'Required Field',
                        'unique': 'duplicated name'},
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100'})
    )

    price = forms.DecimalField(
        error_messages={'required': 'Required Field',
                        'invalid': 'Invalid Price',
                        'min_value': 'It cant be negative price',
                        'max_digits': 'It cant surpass 5 digits',
                        'max_decimal_places': 'More than 2 decimals digits',
                        'max_whole_digits': 'More than 3 integer digits'},
        min_value=0,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'
        })
    )

    quantity = forms.IntegerField(
        min_value=0,
        error_messages={'required': 'Required Field',
                        'min_value': 'It cant be negative in stock'},
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'
        })
    )

    image = forms.ImageField(
        error_messages={'required': 'Required Field',
                        'invalid_image': 'Invalid Image'},
        widget=forms.FileInput(attrs={'class': 'btn btn-outline-warning form-control form-control-sm'})
    )

    cnpj = forms.CharField(
        error_messages={'required': 'Required Field'},
        widget=forms.TextInput({'class': 'form-control form-control-sm',
                                'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'})
    )

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpjAlterado = ''.join(re.findall('\d', str(cnpj)))
        if (not cnpjAlterado) or (len(cnpjAlterado) < 14):
            raise ValidationError("Invalid CNPJ")

        inteiros = list(map(int, cnpjAlterado))
        novo = inteiros[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(novo) < 14:
            r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)
            prod.insert(0, 6)

        if novo == inteiros:
            return cnpj
        raise ValidationError("Invalid CNPJ")
