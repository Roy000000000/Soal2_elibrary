from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from .forms import BookForm
from django.db.models import Q
import os
from django.conf import settings
from .utils import convert_pdf_to_images
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from django.shortcuts import render


@login_required
def preview_book(request, pk, page=1):
    book = get_object_or_404(Book, pk=pk)

    
    images_dir = book.get_converted_images_path()
    if not images_dir or not os.path.exists(images_dir):
        messages.error(request, "Buku belum dikonversi ke gambar.")
        return redirect("book_detail", pk=pk)

    
    all_pages = sorted([f for f in os.listdir(images_dir) if f.endswith(".png")])
    total_pages = len(all_pages)

    
    page = max(1, min(page, total_pages))
    current_page = f"books/pages/{book.id}/page_{page}.png"

    context = {
        "book": book,
        "page": page,
        "total_pages": total_pages,
    }
    return render(request, "books/preview_book.html", context)


@login_required
def analyze_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    text_data = ""
    if book.description:
        text_data += book.description + " "
    if book.title:
        text_data += book.title + " "
    if book.author:
        text_data += book.author + " "

    
    if book.pdf:
        import fitz  # PyMuPDF
        try:
            with fitz.open(book.pdf.path) as doc:
                for page in doc:
                    text_data += page.get_text("text") + " "
        except:
            pass

    
    keywords = []
    if text_data.strip():
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text_data)

        vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
        X = vectorizer.fit_transform([cleaned])
        keywords = vectorizer.get_feature_names_out().tolist()

    context = {
        "book": book,
        "keywords": keywords
    }
    return render(request, "books/analyze_book.html", context)


@require_POST
@login_required
def toggle_favorite(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    book.favorite = not book.favorite
    book.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'favorite': book.favorite})
    
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'book_list'))
    return redirect(next_url)

@method_decorator(login_required, name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.all()
        
        # Filter favorit
        favorite = self.request.GET.get('favorite')
        if favorite == '1':
            queryset = queryset.filter(favorite=True)
        
        # Filter genre
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)
        
        # Filter pencarian
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(author__icontains=q) |
                Q(description__icontains=q) |
                Q(year__icontains=q)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite'] = self.request.GET.get('favorite', '')
        context['genre'] = self.request.GET.get('genre', '')
        context['genre_choices'] = Book.GENRE_CHOICES
        context['q'] = self.request.GET.get('q', '')
        return context

@login_required
def upload_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            
            
            if book.pdf:
                import fitz  # PyMuPDF
                try:
                    with fitz.open(book.pdf.path) as doc:
                        book.pages = doc.page_count
                except:
                    book.pages = None
            
            book.save()
            
            if book.pdf:
                try:
                    pdf_path = book.pdf.path
                    output_dir = os.path.join(settings.MEDIA_ROOT, f"books/pages/{book.id}")
                    os.makedirs(output_dir, exist_ok=True)
                    image_paths = convert_pdf_to_images(pdf_path, output_dir)
                    messages.success(request, "Buku berhasil diupload dan dikonversi!")
                except Exception as e:
                    messages.warning(request, f"Buku berhasil diupload tetapi konversi gagal: {str(e)}")
            else:
                messages.success(request, "Buku berhasil diupload!")
                
            return redirect("book_list")
        else:
            messages.error(request, "Upload gagal, periksa kembali form.")
    else:
        form = BookForm()
    return render(request, "books/upload_book.html", {"form": form})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/book_detail.html", {"book": book})

@login_required
def search_books(request):
    query = request.GET.get('q', '')
    
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query) |
            Q(year__icontains=query)
        )
    else:
        books = Book.objects.none()
    
    # Pagination
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'books': page_obj,
        'query': query,
        'is_paginated': paginator.num_pages > 1,
        'genre_choices': Book.GENRE_CHOICES
    }
    
    return render(request, "books/book_list.html", context)

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.user != book.uploaded_by and not request.user.is_superuser:
        messages.error(request, "Anda tidak memiliki izin untuk menghapus buku ini.")
        return redirect('book_list')

    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f"Buku '{book_title}' berhasil dihapus.")
        return redirect('book_list')

    return redirect('book_detail', pk=book.pk)


@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.user != book.uploaded_by and not request.user.is_superuser:
        messages.error(request, "Anda tidak punya izin untuk edit buku ini.")
        return redirect('book_list')

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            updated_book = form.save(commit=False)

            if 'pdf' in form.changed_data and updated_book.pdf:
                import fitz
                try:
                    with fitz.open(updated_book.pdf.path) as doc:
                        updated_book.pages = doc.page_count
                except:
                    updated_book.pages = None

            updated_book.save()
            messages.success(request, "Buku berhasil diperbarui!")
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, "books/upload_book.html", {"form": form, "book": book})
