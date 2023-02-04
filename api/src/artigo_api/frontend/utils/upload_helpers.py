import os

import numpy as np

from PIL import Image
from pathlib import Path

Image.MAX_IMAGE_PIXELS = 10000 * 10000


def resize_image(img, max_dim=None, min_dim=None):
    shape = np.asarray(img.shape[:2], dtype=np.float32)

    if max_dim is not None:
        scale = min(1, max_dim / max(shape))
    elif min_dim is not None:
        scale = max(1, min_dim / min(shape))
    else:
        return img
        
    shape = np.asarray(shape * scale, dtype=np.int32)
    img = Image.fromarray(img).resize(size=shape[::-1])

    return np.array(img)


def check_extension(file_path, extensions=None):
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if extensions is not None:
        file_extension = ''.join(file_path.suffixes).lower()

        for extension in extensions:
            if file_extension.endswith(extension.lower()):
                return True

    return False


def download_file(file, output_dir, output_name=None, max_size=None, extensions=None):
    try:
        file_name = file.name
        file_path = Path(file_name)

        if output_name is not None:
            file_extension = ''.join(file_path.suffixes).lower()
            file_name = f'{output_name}{file_extension}'
            
        output_path = os.path.join(output_dir, f'{file_name}')

        if extensions is not None:
            if not check_extension(file_path, extensions):
                return {
                    'status': 'error',
                    'error': {
                        'type': 'file_extension_is_invalid',
                    },
                }

        if max_size is not None:
            if file.size > max_size:
                return {
                    'status': 'error',
                    'error': {
                        'type': 'file_is_too_large',
                    },
                }

        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'wb') as file_obj:
            for chunk in file.chunks():
                file_obj.write(chunk)

        return {
            'status': 'ok',
            'path': Path(output_path),
            'origin': file.name,
        }
    except:
        return {
            'status': 'error',
            'error': {
                'type': 'unknown_error',
            },
        }
