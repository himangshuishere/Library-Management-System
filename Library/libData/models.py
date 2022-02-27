import uuid
from django.urls import reverse
from django.db import models

# Create your models here.

class UsersModel(models.Model):
    userId = models.CharField(default=str(uuid.uuid4().hex).replace('-', ''), editable=False, primary_key=True, max_length=50)
    userName = models.CharField(max_length=50)
    userEmail = models.EmailField(max_length=50, unique=True)
    userPassword = models.CharField(max_length=50)

    def __str__(self):
        return self.userName
    
    class Meta:
        verbose_name_plural = "Users"


class BooksModel(models.Model):
    bookID = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    bookName = models.CharField(max_length=50)
    bookAuthor = models.CharField(max_length=50)
    bookDescription = models.TextField(max_length=500)

    def __str__(self):
        return self.bookName
    
    def get_absolute_url(self):
        return reverse("book-Detail", args=[self.bookID])
    
    
    class Meta:
        verbose_name_plural = "Books"

class IssuedBooksModel(models.Model):
    issuedBy = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    issuedBook = models.ForeignKey(BooksModel, on_delete=models.CASCADE)
    issuedDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.issuedBook.bookName

    class Meta:
        verbose_name_plural = "Issued Books"