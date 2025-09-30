import os

from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm
from django.utils.translation import gettext_lazy as _

from catalog.constants import ValidationConstants
from catalog.models import Product


class StyleFormMixin:
    """Mixin для стилизации полей формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = _("Введите название продукта")
        self.fields["description"].widget.attrs["placeholder"] = _("Описание продукта")
        self.fields["price"].widget.attrs["placeholder"] = _("Цена")
        self.fields["category"].widget.attrs["placeholder"] = _("Выберите категорию")

    def clean_price(self):
        """Валидация цены с проверками"""
        price = self.cleaned_data.get("price")

        if price is None:
            raise ValidationError(
                ValidationConstants.ERROR_MESSAGES["none_price"], code="none_price"
            )

        if price < ValidationConstants.MIN_PRICE:
            raise ValidationError(
                ValidationConstants.ERROR_MESSAGES["negative_price"],
                code="negative_price",
            )

        return price

    def clean_name(self):
        name = self.cleaned_data["name"]
        for banned_word in ValidationConstants.FORBIDDEN_WORDS:
            if banned_word in name.lower():
                raise ValidationError("Нельзя использовать запрещенные слова")
            elif name and len(name) < 3:
                raise ValidationError(
                    ValidationConstants.ERROR_MESSAGES["name_too_short"],
                    code="name_too_short",
                )
            elif name and len(name) > 100:
                raise ValidationError(
                    ValidationConstants.ERROR_MESSAGES["name_too_long"],
                    code="name_too_long",
                )
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        for banned_word in ValidationConstants.FORBIDDEN_WORDS:
            if banned_word in description.lower():
                raise ValidationError("Нельзя использовать запрещенные слова")
        return description

    def clean_image(self):
        """Валидация изображения"""

        image = self.cleaned_data.get("image")
        if image:
            if image.size > ValidationConstants.MAX_IMAGE_SIZE:
                raise ValidationError(
                    ValidationConstants.ERROR_MESSAGES["image_size"],
                    code="image_size_exceeded",
                )
            else:
                ext = os.path.splitext(image.name)[1].lower().lstrip(".")
                if ext not in ValidationConstants.ALLOWED_IMAGE_EXTENSIONS:
                    raise ValidationError(
                        ValidationConstants.ERROR_MESSAGES["image_format"],
                        code="invalid_image_format",
                    )
                else:
                    return image
        else:
            raise ValidationError(
                        ValidationConstants.ERROR_MESSAGES["image_corrupted"],
                        code="image_corrupted",
                    )
