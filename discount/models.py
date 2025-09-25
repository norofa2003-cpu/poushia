from django.db import models
from django.utils import timezone

class DiscountCode(models.Model):
    code = models.CharField("کد تخفیف", max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField("درصد تخفیف")
    is_active = models.BooleanField("فعال است", default=True)
    expires_at = models.DateTimeField("تاریخ انقضا", null=True, blank=True)

    usage_limit = models.PositiveIntegerField("محدودیت استفاده", null=True, blank=True)
    used_count = models.PositiveIntegerField("تعداد استفاده‌شده", default=0)

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"
        ordering = ['-expires_at']

    def str(self):
        return f"{self.code} - {self.discount_percent}%"

    def is_valid(self):
        return self.is_active and \
               (self.expires_at is None or self.expires_at > timezone.now()) and \
               (self.usage_limit is None or self.used_count < self.usage_limit)