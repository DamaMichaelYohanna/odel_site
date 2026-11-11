import os
import shutil
from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Auto-mirror essential static default images into media directory
        # so freshly cloned repositories immediately have all hero banners,
        # leadership portraits, and staff images available.
        try:
            media_root = settings.MEDIA_ROOT
            static_img = settings.BASE_DIR / 'static' / 'images'
            for folder in ['banners', 'leadership', 'staff']:
                src_dir = static_img / folder
                dst_dir = media_root / folder
                if src_dir.exists():
                    os.makedirs(dst_dir, exist_ok=True)
                    for item in os.listdir(src_dir):
                        src_file = src_dir / item
                        dst_file = dst_dir / item
                        if src_file.is_file() and not dst_file.exists():
                            shutil.copy2(src_file, dst_file)
        except Exception:
            pass
