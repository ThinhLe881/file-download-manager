import argparse
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # if file already exists, add a number to the end of the file name
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # supported image types
    image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", 
                        ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", 
                        ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", 
                        ".svg", ".svgz", ".ai", ".eps", ".ico"]
    # supported Video types
    video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                        ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
    # supported Audio types
    audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
    # supported Document types
    document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
    # supported Compressed types
    compressed_extensions = [".rar", ".arj", ".tar.gz", ".tgz", ".gz", ".iso", ".7z", ".zip", ".zipx", ".z"]

    def __init__(self, src_dir, dest_dir_music, dest_dir_video, dest_dir_image, 
                    dest_dir_document, dest_dir_compressed, dest_dir_program):
        self.src_dir = src_dir
        self.dest_dir_music = dest_dir_music
        self.dest_dir_video = dest_dir_video
        self.dest_dir_image = dest_dir_image
        self.dest_dir_document = dest_dir_document
        self.dest_dir_compressed = dest_dir_compressed
        self.dest_dir_program = dest_dir_program

    # this function is called when there is a change in the source directory
    # .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(self.src_dir) as entries:
            for entry in entries:
                name = entry.name
                print(name)
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_compressed_files(entry, name)
                self.check_program_files(entry, name)

    def check_audio_files(self, entry, name):  # checks all Audio files
        for audio_extension in self.audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(self.dest_dir_music, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # checks all Video files
        for video_extension in self.video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(self.dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # checks all Image files
        for image_extension in self.image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(self.dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # checks all Document files
        for document_extension in self.document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_file(self.dest_dir_document, entry, name)
                logging.info(f"Moved document file: {name}")
    
    def check_compressed_files(self, entry, name):  # checks all Compressed files
        for compressed_extension in self.compressed_extensions:
            if name.endswith(compressed_extension) or name.endswith(compressed_extension.upper()):
                move_file(self.dest_dir_compressed, entry, name)
                logging.info(f"Moved compressed file: {name}")

    def check_program_files(self, entry, name):  # checks all Program files
        if name.endswith(".exe") or name.endswith(".EXE"):
            move_file(self.dest_dir_program, entry, name)
            logging.info(f"Moved program file: {name}")


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    parser = argparse.ArgumentParser(description='File Manager')
    parser.add_argument('src_dir', metavar='src_path', type=str, help='The directory that need to manage')
    parser.add_argument('dest_dir_music', metavar='dest_dir_music', type=str, help='The directory for music/audio files')
    parser.add_argument('dest_dir_video', metavar='dest_dir_video', type=str, help='The directory for video files')
    parser.add_argument('dest_dir_image', metavar='dest_dir_image', type=str, help='The directory for image files')
    parser.add_argument('dest_dir_document', metavar='dest_dir_documents', type=str, help='The directory for document files')
    parser.add_argument('dest_dir_compressed', metavar='dest_dir_compressed', type=str, help='The directory for compressed files')
    parser.add_argument('dest_dir_program', metavar='dest_dir_program', type=str, help='The directory for executable file')
    args = parser.parse_args()

    src_dir = args.src_dir
    dest_dir_music = args.dest_dir_music
    dest_dir_video = args.dest_dir_video
    dest_dir_image = args.dest_dir_image
    dest_dir_document = args.dest_dir_document
    dest_dir_compressed = args.dest_dir_compressed
    dest_dir_program = args.dest_dir_program

    event_handler = MoverHandler(src_dir, dest_dir_music, dest_dir_video, dest_dir_image, 
                                    dest_dir_document, dest_dir_compressed, dest_dir_program)
    observer = Observer()
    observer.schedule(event_handler, src_dir, recursive=True)
    observer.start()
    print("Watching for changes in the source directory...")
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
