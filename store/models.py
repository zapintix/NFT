from django.db import models


class Nft(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    typePrice = models.ForeignKey('TypePrice', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='product_image/', blank=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)
    autor = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TypePrice(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
