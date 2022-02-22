import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Books(models.Model):
    id = models.UUIDField(default=uuid.uuid4, blank=True, editable=False, primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    slug = models.SlugField(default="", blank=True, null=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("bookDetail", args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Books"

class IssuedBooks(models.Model):
    issueID = models.UUIDField(default=uuid.uuid4, blank=True, editable=False, primary_key=True)
    issuer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    issuedBook = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, related_name='book')
    issuedAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.issuer.email
    
    class Meta:
        verbose_name_plural = 'Issued Books'