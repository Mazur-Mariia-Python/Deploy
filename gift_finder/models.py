from django.db import models
from Tobi import settings


#A model that is needed to save links to a category of a certain product and pass this link to the parser
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва товару')
    link = models.URLField(verbose_name='Посилання на товар')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'


"""Model for saving selected gifts"""


class SelectedGift(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=30)
    image_url = models.TextField(help_text="URL of the image for the gift.")
    link = models.TextField(help_text="URL to purchase the gift.")
    is_bought = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    """Sorting selected gifts from newest to oldest"""
    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Selected gifts"

    def __str__(self):
        return str(self.name)
