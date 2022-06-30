import sys
from pathlib import Path
# изображения
JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
# видео файлы
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
# DOCUMENTS
DOC_DOCUM = []
DOCX_DOCUM = []
TXT_DOCUM = []
PDF_DOCUM = []
XLSX_DOCUM = []
PPTX_DOCUM = []
# MUSIC
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
# ARCHIVES
ARCHIVES = []

OTHER = []
FOLDERS = []

REGISTER_EXTENSIONS = {
    # изображения
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    # видео файлы
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    # DOCUMENTS
    'DOC': DOC_DOCUM,
    'DOCX': DOCX_DOCUM,
    'TXT': TXT_DOCUM,
    'PDF': PDF_DOCUM,
    'XLSX': XLSX_DOCUM,
    'PPTX': PPTX_DOCUM,
    # MUSIC
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    # ARCHIVES
    'ZIP': ARCHIVES,
    'TAR': ARCHIVES,
    'GZ': ARCHIVES

}

EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("archives", "video", "audio", "documents", "images", "OTHER"):
                FOLDERS.append(item)
                scan(item)
            continue
        ext = get_extension(item.name)
        fullname = folder / item.name
        if not ext:
            OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                OTHER.append(fullname)


if __name__ == "__main__":
    path = Path(sys.argv[1])
    print(scan(path))
    for k, v in REGISTER_EXTENSIONS.items():
        print('\n')
        print(k, v)
        print('\n')
