rem render_badminton.bat T:\VideoEdit\Goodminton-20221116\raw\
python render_proj.py %1
python join_clips.py %1clips/
pause
set openme="%~1clips"
explorer %openme%
pipenv run python upload_youtube.py %1clips/output.mp4