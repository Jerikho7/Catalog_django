from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product

BLACK_LIST = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Введите {field.label.lower()}'
            })

    def clean(self):
        cleaned_data = super().clean()
        name_product = cleaned_data.get("name_product")
        description = cleaned_data.get("description")

        for word in BLACK_LIST:
            if word in name_product.lower() or word in description.lower():
                self.add_error(
                    "name_product", f"В названии товара не должно быть включено запрещенное слово - {word}."
                )
                self.add_error("description", f"В описании товара не должно быть включено запрещенное слово - {word}.")

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не должна быть меньше нуля")
        elif price is None:
            raise ValidationError("Цена должна быть указана")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        max_size = 5 * 1024 * 1024

        if image.size > max_size:
            raise ValidationError(
                f"Файл слишком большой. Максимальный размер: {max_size / 1024 / 1024} МБ"
            )
        elif not image.name.endswith((".jpg", ".jpeg", ".png")):
            raise ValidationError(
                "Неподдерживаемый формат файла. Используйте JPEG или PNG."
            )
        return image