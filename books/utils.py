import fitz  # PyMuPDF
import os
from PIL import Image
from django.conf import settings

def convert_pdf_to_images(pdf_path, output_dir, dpi=150):
    """
    Convert PDF to images using PyMuPDF
    Returns list of image paths
    """
    image_paths = []
    
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            # Get the page
            page = doc.load_page(page_num)
            
            # Convert to image
            mat = fitz.Matrix(dpi / 72, dpi / 72) 
            pix = page.get_pixmap(matrix=mat)
            
            # Save as PNG
            img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
            pix.save(img_path)
            image_paths.append(img_path)
        
        doc.close()
        return image_paths
        
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []