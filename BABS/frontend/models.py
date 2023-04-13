from django.db import models


class ScanResults(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    symbol = models.CharField(max_length=9, blank=True, null=True)
    bids = models.JSONField(blank=True, null=True)
    asks = models.JSONField(blank=True, null=True)