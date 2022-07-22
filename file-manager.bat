@echo off
set src_dir=""
set dest_dir_music=""
set dest_dir_video=""
set dest_dir_image=""
set dest_dir_documents=""
set dest_dir_compressed=""
set dest_dir_program=""
cd /d ""
python file_manager.py %src_dir% %dest_dir_music% %dest_dir_video% %dest_dir_image% %dest_dir_documents% %dest_dir_compressed% %dest_dir_program%