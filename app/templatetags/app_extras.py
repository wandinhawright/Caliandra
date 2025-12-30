"""
Custom template tags for the app.
"""
import json
import os
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def vite_asset(entry_name):
    """
    Get the built asset paths from Vite's manifest.json.
    
    Args:
        entry_name: The entry name in manifest (e.g., 'index.html')
    
    Returns:
        Dict with 'js' and 'css' keys containing the asset paths
    """
    manifest_path = os.path.join(
        settings.BASE_DIR,
        'app',
        'static',
        'app',
        'dist',
        '.vite',
        'manifest.json'
    )
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        entry = manifest.get(entry_name, {})
        
        return {
            'js': entry.get('file', ''),
            'css': entry.get('css', [''])[0] if entry.get('css') else ''
        }
    except (FileNotFoundError, json.JSONDecodeError):
        # During development or before build
        return {
            'js': '',
            'css': ''
        }
