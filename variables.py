IMAGE_EXTENSIONS_LOWER = ("png", "jpg", "jpeg", "gif")
VIDEO_EXTENSIONS_LOWER = ("mp4", "avi", "mov")
IMAGE_EXTENSIONS = IMAGE_EXTENSIONS_LOWER + tuple(ext.upper() for ext in IMAGE_EXTENSIONS_LOWER)
VIDEO_EXTENSIONS = VIDEO_EXTENSIONS_LOWER + tuple(ext.upper() for ext in VIDEO_EXTENSIONS_LOWER)
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS
MEDIA_COLUMN_WIDTH = 4

CAPTION_PATH_OPTIONS = ["none"]
