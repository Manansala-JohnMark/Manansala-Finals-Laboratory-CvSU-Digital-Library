from django.db import models
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True
    )
    publication_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        authors_list = ", ".join(str(author) for author in self.authors.all())
        return f"{self.title} by {authors_list}" if authors_list else self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})


class BookCopy(models.Model):

    COPY_TYPES = [
        ("Printed", "Printed"),
        ("PDF", "PDF"),
        ("eBook", "eBook"),
    ]

    AVAILABILITY = [
        ("Available", "Available"),
        ("Reference Only", "Reference Only"),
        ("Unavailable", "Unavailable"),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='copies'
    )
    copy_number = models.PositiveIntegerField()
    copy_type = models.CharField(
        max_length=50,
        choices=COPY_TYPES
    )
    availability_status = models.CharField(
        max_length=50,
        choices=AVAILABILITY,
        default="Available"   # IMPORTANT for migrations
    )

    class Meta:
        unique_together = ('book', 'copy_number')
        ordering = ['copy_number']

    def __str__(self):
        return f"{self.book.title} – Copy {self.copy_number} ({self.copy_type})"
