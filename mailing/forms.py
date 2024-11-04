from django import forms

from mailing.models import Recipient


class RecipientForm(forms.ModelForm):
    """Класс формы клиента"""

    class Meta:
        model = Recipient
        fields = ["full_name", "email", "comments"]

#     def __init__(self, *args, **kwargs):
#         super(RecipientForm, self).__init__(*args, **kwargs)
#
#         if "image" in self.fields:
#             self.fields["image"].widget.attrs.update(
#                 {
#                     "class": "form-control",
#                 }
#             )
#
#         self.fields["name"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Введите название продукта"}
#         )
#
#         self.fields["description"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Введите описание продукта"}
#         )
#
#         self.fields["category"].widget.attrs.update(
#             {
#                 "class": "form-control",
#             }
#         )
#
#         self.fields["price"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Введите стоимость"}
#         )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get("name")
#         description = cleaned_data.get("description")
#
#         if name.lower() and description.lower() in [
#             "казино",
#             "криптовалюта",
#             "крипта",
#             "биржа",
#             "дешево",
#             "бесплатно",
#             "обман",
#             "полиция",
#             "радар",
#         ]:
#             self.add_error("name", "запрещенное слово")
#             self.add_error("description", "запрещенное слово")
#
#     def clean_price(self):
#         cleaned_data = super().clean()
#         price = cleaned_data.get("price")
#
#         if price is None:
#             raise forms.ValidationError("Цена должна быть указана.")
#
#         if price < 0:
#             raise forms.ValidationError("Цена не может быть отрицательной.")
#
#         return price
#
#     def clean_image(self):
#         cleaned_data = super().clean()
#         if "image" in cleaned_data:
#             image = cleaned_data.get("image")
#             if image.size > 5 * 1024 * 1024:
#                 raise forms.ValidationError("Размер файла не должен превышать 5 МБ.")
#             if not image.name.endswith(("jpg", "jpeg", "png")):
#                 raise forms.ValidationError(
#                     "Недопустимый формат файла. Загрузите JPEG или PNG."
#                 )
#             return image
#         else:
#             raise forms.ValidationError("Изображение должно быть указано.")
#
#
# class ProductModeratorForm(forms.ModelForm):
#
#     class Meta:
#
#         model = Product
#         fields = ["status"]
