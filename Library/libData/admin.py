from django.contrib import admin
from .models import UsersModel, BooksModel, IssuedBooksModel

# Register your models here.

admin.site.register(UsersModel)
# class UsersModelAdmin(admin.ModelAdmin):
    # list_display = ('userId',)

@admin.register(BooksModel)
class BooksModelAdmin(admin.ModelAdmin):
    list_display = ('bookID', 'bookName', 'bookAuthor', 'bookDescription')
    list_filter = ('bookAuthor',)
    search_fields = ('bookName', 'bookAuthor')

class IssuedBooksModelAdmin(admin.ModelAdmin):
    list_display = ('issuedBook', 'issuedBy')
admin.site.register(IssuedBooksModel, IssuedBooksModelAdmin)