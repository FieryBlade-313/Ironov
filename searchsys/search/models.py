from django.db import models

# Create your models here.
class Recent(models.Model):
    doc_id = models.IntegerField(default=1,verbose_name='Document ID')
    cosine_score = models.FloatField(default=1.0,verbose_name='Cosine Score')

    def __str__(self):
        return str(self.doc_id)