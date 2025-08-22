import os
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def file_exists(file_path):
    """
    Check if a file exists in the filesystem
    Usage: {{ file_path|file_exists }}
    """
    if not file_path:
        return False
    
   
    if not os.path.isabs(file_path):
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    else:
        full_path = file_path
    
    return os.path.exists(full_path)

@register.filter
def get_file_url(file_path):
    """
    Get MEDIA_URL for file path if exists
    Usage: {{ file_path|get_file_url }}
    """
    if file_path and file_exists(file_path):
        return os.path.join(settings.MEDIA_URL, file_path)
    return ""

@register.filter
def basename(file_path):
    """Get basename of file path"""
    return os.path.basename(file_path) if file_path else ""

@register.filter
def filesize(file_path):
    """Get file size if exists"""
    if file_path and file_exists(file_path):
        size = os.path.getsize(os.path.join(settings.MEDIA_ROOT, file_path))
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.1f} MB"
    return "0 B"