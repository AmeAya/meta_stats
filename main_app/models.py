from django.db import models
from django.utils import timezone


class MetaAdInsight(models.Model):
    ad_id = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    campaign_id = models.CharField(max_length=255)
    campaign_name = models.CharField(max_length=255)
    adset_name = models.CharField(max_length=255)
    ad_name = models.CharField(max_length=255)

    spend = models.DecimalField(max_digits=12, decimal_places=2)
    impressions = models.PositiveIntegerField()
    reach = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()
    cpc = models.DecimalField(max_digits=16, decimal_places=6)
    cpm = models.DecimalField(max_digits=16, decimal_places=6)
    frequency = models.DecimalField(max_digits=16, decimal_places=6)

    lead_count_form = models.PositiveIntegerField(default=0)
    lead_count_message = models.PositiveIntegerField(default=0)

    raw_actions = models.JSONField(null=True, blank=True)

    date = models.CharField(max_length=12)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Meta Ad Insight"
        verbose_name_plural = "Meta Ad Insights"

    def __str__(self):
        return f"{self.campaign_name} - {self.ad_name}"
