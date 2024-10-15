import os
import re

def sanitize_filename(filename):
    """Sanitize filenames by removing or replacing characters not safe for filenames."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)
