from django.db import models


class ScanResults(models.Model):
    symbol = models.CharField(max_length=9, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    bids = models.JSONField(blank=True, null=True)
    asks = models.JSONField(blank=True, null=True)