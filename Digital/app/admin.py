from django.contrib import admin
from .models import Book, Author, Publisher, Category, BookCopy

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(BookCopy)
# Register your models here.
