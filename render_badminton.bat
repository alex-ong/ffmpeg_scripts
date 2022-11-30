rem render_badminton.bat T:/VideoEdit/Goodminton-20221116/raw/
python render_proj.py %1
python join_clips.py %1/clips/
explorer %1/clips/