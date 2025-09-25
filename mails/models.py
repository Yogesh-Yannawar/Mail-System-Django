from django.db import models

# Create your models here.
class Mail(models.Model):
    from_user = models.CharField(max_length=50)
    to_user = models.CharField(max_length=50)
    subject =models.CharField(max_length=200)
    mail_content=models.CharField(max_length=4000)
    datetime = models.DateTimeField()
    attachment=models.FileField(upload_to='attachments/',blank=True)

