from django.db import models
from django.urls import reverse
from category.models import Category
from accounts.models import Account

class Product(models.Model):
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    brand_name = models.CharField(max_length=30, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=255)
    price = models.DecimalField(
        verbose_name="Regular price",
        help_text="Maximum 99999.99",
        error_messages={
            "name": {
                "max_length": "The price must be between 0 and 999999.99.",
            },
        },
        max_digits=7,
        decimal_places=2,
    )
    discount_percentage = models.IntegerField(default=0, blank=True)
    product_image = models.ImageField(upload_to='static/img')
    alt_text = models.CharField(max_length=200)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_trending = models.BooleanField(default=False)
    is_topSelling = models.BooleanField(default=False)
    logo_image = models.ImageField(upload_to='static/img', blank=True)
    logo_altText = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def discountPrice(self):
        if self.discount_percentage > 0:
            theprice = self.price - ((self.price * self.discount_percentage) / 100)
            return round(theprice, 2)
    discount_price = property(discountPrice)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=300, blank=True)
    rating = models.IntegerField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

