import json

import django.forms as forms
from django.core.validators import FileExtensionValidator

from .models import Product


def file_size_validator(value):
    if value.size > 5242880:
        raise forms.ValidationError("Файл должен быть меньше 5 МБ")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image", "is_published"]

    def clean_price(self) -> float:
        """
        Валидация цены
        
        Returns:
            float:
        """
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price

    def clean_name(self):
        """
        Валидация имени продукта


        Raises:
            forms.ValidationError: Недопустимое слово
            
        Returns:
            str:
        """
        with open("black_list_words.json", "r", encoding="utf-8") as f:
            words = json.load(f)

        name = self.cleaned_data["name"]

        for word in words:
            if word in name.lower().split():
                raise forms.ValidationError(f"Недопустимое слово: {word}")

        return name
    
    def clean_description(self):
        """
        Валидация описания продукта


        Raises:
            forms.ValidationError: Недопустимое слово
            
        Returns:
            str:
        """
        with open("black_list_words.json", "r", encoding="utf-8") as f:
            words = json.load(f)

        description = self.cleaned_data["description"]

        for word in words:
            if word in description.lower().split():
                raise forms.ValidationError(f"Недопустимое слово: {word}")

        return description

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Для всех полей формы добавляем классы Bootstrap
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "Введите " + field.label

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"

            if field_name == "is_published":
                field.label = "Опубликовать"

            if field_name == "image":
                field.widget.attrs["class"] = "form-control"

            # Если у поля есть ошибки, добавляем класс is-invalid
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"

        # Добавляем специфические валидаторы для файла
        self.fields["image"].validators = [
            FileExtensionValidator(allowed_extensions=["jpg", "png"], message="Неверное расширение файла"),
            file_size_validator,
        ]
