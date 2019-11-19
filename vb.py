import visbeat

source_url = 'https://www.youtube.com/watch?v=ZfICRzbt-ZY'
target_url = 'https://www.youtube.com/watch?v=VdXZaGGWe3Y' # YUM! YUM! BREAKFAST BURRITO!

output_path = './MyFunnyVideo.mp4'

result = visbeat.AutoDancefer(source=source_url, target = target_url, 
                              output_path = output_path,
                              synch_video_beat = 0,
                              synch_audio_beat = 0,
                              beat_offset = 0,
                             nbeats = 440)