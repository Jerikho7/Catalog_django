from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    name_product = models.CharField(max_length=150, verbose_name="Наименование товара")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to="catalog/image", blank=True, null=True, verbose_name="Изображение продукта")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="Категории",
        verbose_name="Категория",
    )
    price = models.IntegerField(verbose_name="Стоимость")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата последнего изменения")

    is_published = models.BooleanField(verbose_name="Статус публикации", default="False")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="Владелец",
        verbose_name="Владелец",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"'Наименование - {self.name_product}. Цена - {self.price}."

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name_product"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
        ]
