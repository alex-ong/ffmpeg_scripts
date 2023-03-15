for %%f in (*.mp4) do (
    echo file %%f >> list.txt
)
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
del list.txt