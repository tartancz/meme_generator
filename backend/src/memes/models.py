from django.db import models

# Create your models here.

class MemeTemplate(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    low_res = models.ImageField(upload_to="memes/template/low_res", blank=False, null=False)
    high_res = models.ImageField(upload_to="memes/template/high_res", blank=False, null=False)

class Meme(models.Model):
    low_res = models.ImageField(upload_to="memes/meme/low_res", blank=False, null=False)
    high_res = models.ImageField(upload_to="memes/meme/high_res", blank=False, null=False)
    bottom_text = models.CharField(max_length=200, blank=True)
    top_text = models.CharField(max_length=200, blank=True)
    private = models.BooleanField(default=True)
    template = models.ForeignKey(MemeTemplate, on_delete=models.CASCADE, related_name="memes")