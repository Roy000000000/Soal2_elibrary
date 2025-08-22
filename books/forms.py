from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf', 'title', 'description', 'author', 'year', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Buku'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Deskripsi buku'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Penulis'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tahun Terbit'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'pdf': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }
        labels = {
            'pdf': 'File PDF',
            'title': 'Judul',
            'description': 'Deskripsi',
            'author': 'Penulis',
            'year': 'Tahun Terbit',
            'genre': 'Genre',
        }
    
    def clean_pdf(self):
        pdf = self.cleaned_data.get('pdf')
        if pdf:
            if not pdf.name.endswith('.pdf'):
                raise forms.ValidationError("Hanya file PDF yang diperbolehkan.")
        return pdf