from django.db import models


class Symbol(models.Model):
    symbol = models.CharField(blank=True, null=True)


class ScanResults(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=True, null=True)
    bids = models.JSONField(blank=True, null=True)
    asks = models.JSONField(blank=True, null=True)