from django.db import models

# Create your models here.
from django.db import models

class StockTrace(models.Model):
    stock1 = models.CharField(max_length=10)
    stock2 = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    window_size = models.IntegerField()

    def __str__(self):
        return f"Trace {self.stock1} vs {self.stock2} ({self.start_date} - {self.end_date})"