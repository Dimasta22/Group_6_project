from pathlib import Path
import shutil
import sys
import filewalker as parser
from normalize import normalize


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archives(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Folder {folder} hasn`t deleted")


def is_folder(path: str):
    path = Path(path.replace('\\', '/'))
    if path.is_dir():
        return path
    else:
        return False


def sort(folder: str):
    folder = is_folder(folder)
    if folder == False:
        return 'Path not correct'
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')
    for file in parser.DOC_DOCUM:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_DOCUM:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in parser.TXT_DOCUM:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in parser.PDF_DOCUM:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in parser.XLSX_DOCUM:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in parser.PPTX_DOCUM:
        handle_media(file, folder / 'documents' / 'PPTX')
    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')
        # other
    for file in parser.OTHER:
        handle_other(file, folder / 'OTHERS')
        # archives
    for file in parser.ARCHIVES:
        handle_archives(file, folder / 'archives')
        # folder
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)
    return 'Your folder is sorted'


if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'strart in folder {folder_for_scan.resolve()}')
        sort(folder_for_scan.resolve())
