from django.db import models


# device object
class Device(models.Model):
    device = models.CharField(max_length=250)
    deviceType = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    vendor = models.CharField(max_length=250)

    def __str__(self):
        return 'Device: {}'.format(self.device)