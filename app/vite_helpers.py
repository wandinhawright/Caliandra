"""
Helper functions for integrating Vite build output with Django templates.
"""
import json
import os
from django.conf import settings


def get_vite_manifest():
    """
    Read the Vite manifest.json file to get the built asset filenames.
    This is needed because Vite adds content hashes to filenames in production.
    """
    manifest_path = os.path.join(
        settings.BASE_DIR,
        'app',
        'static',
        'app',
        'dist',
        'manifest.json'
    )
    
    try:
        with open(manifest_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # During development or before build, manifest doesn't exist
        return {}


def get_vite_asset(entry_name='src/main.js'):
    """
    Get the built asset filename for a given entry point.
    
    Args:
        entry_name: The source file path (e.g., 'src/main.js')
    
    Returns:
        Dict with 'css' and 'js' keys containing the built asset paths
    """
    manifest = get_vite_manifest()
    
    if not manifest:
        # Development mode - use Vite dev server
        return {
            'js': 'http://localhost:5173/src/main.js',
            'css': None
        }
    
    entry = manifest.get(entry_name, {})
    
    return {
        'js': entry.get('file'),
        'css': entry.get('css', [None])[0] if entry.get('css') else None
    }
