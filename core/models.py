from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ads/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Hero Ad'
        verbose_name_plural = 'Hero Ads'

    def __str__(self):
        return self.title


class SideAd(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='side_ads/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Side Ad'
        verbose_name_plural = 'Side Ads'

    def __str__(self):
        return self.title


class BannerAd(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banner_ads/')
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Banner Ad'
        verbose_name_plural = 'Banner Ads'

    def __str__(self):
        return self.title


class CardAd(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='card_ads/')
    link = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Card Ad'
        verbose_name_plural = 'Card Ads'

    def __str__(self):
        return self.title

    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price
