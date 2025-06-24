from youtube_transcript_api import YouTubeTranscriptApi

video_id = "3zxMmPkkn6M"

ytt_api = YouTubeTranscriptApi()
trans = ytt_api.fetch(video_id)
assert trans