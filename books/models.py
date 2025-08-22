from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.conf import settings
from django.utils import timezone


class Book(models.Model):
    GENRE_CHOICES = [
        ("fiksi", "Fiksi"),
        ("komik", "Komik"),
        ("motivasi", "Motivasi"),
    ]

    title = models.CharField(max_length=200, verbose_name="Judul")
    description = models.TextField(verbose_name="Deskripsi", blank=True)
    author = models.CharField(max_length=100, verbose_name="Penulis", blank=True)
    year = models.IntegerField(verbose_name="Tahun Terbit", null=True, blank=True)

    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        default="fiksi",
        verbose_name="Genre"
    )

    pages = models.IntegerField(verbose_name="Jumlah Halaman", null=True, blank=True)

    pdf = models.FileField(
        upload_to="books/pdfs/",
        verbose_name="File PDF",
        null=True,
        blank=True
    )

    cover = models.ImageField(
        upload_to="books/covers/",
        verbose_name="Cover Buku",
        null=True,
        blank=True,
        help_text="Upload cover buku (opsional)"
    )

    favorite = models.BooleanField(default=False, verbose_name="Favorit")

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Diupload oleh",
        related_name="uploaded_books"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

    def get_genre_display(self):
        return dict(self.GENRE_CHOICES).get(self.genre, self.genre)

    def file_exists(self):
        if self.pdf:
            return os.path.exists(self.pdf.path)
        return False

    def cover_exists(self):
        if self.cover:
            return os.path.exists(self.cover.path)
        return False

    def get_cover_url(self):
        if self.cover and self.cover_exists():
            return self.cover.url
        return None

    def get_pdf_url(self):
        if self.pdf and self.file_exists():
            return self.pdf.url
        return None

    def get_converted_images_path(self):
        if self.pdf:
            return os.path.join(settings.MEDIA_ROOT, f"books/pages/{self.id}/")
        return None

    def has_converted_images(self):
        images_path = self.get_converted_images_path()
        if images_path and os.path.exists(images_path):
            return len(os.listdir(images_path)) > 0
        return False

    def get_first_page_image(self):
        if self.has_converted_images():
            return settings.MEDIA_URL+ f"books/pages/{self.id}/page_1.png"
        return None

    class Meta:
        verbose_name = "Buku"
        verbose_name_plural = "Buku"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['genre']),
            models.Index(fields=['favorite']),
            models.Index(fields=['created_at']),
        ]
