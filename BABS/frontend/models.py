from django.db import models


class ScanResults(models.Model):
    json_data = models.JSONField(blank=True, null=True)