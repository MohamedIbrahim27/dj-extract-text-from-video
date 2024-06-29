import moviepy.editor as mp
import speech_recognition as sr
from pytube import YouTube
import os
# Define paths
youtube_url = 'https://www.youtube.com/watch?v=ry9SYnV3svc&ab_channel=LearnEnglishbyPocketPassport'
video_output_path = 'downloaded_audio.mp4'
audio_output_path = 'extracted_audio.wav'

def download_youtube_audio(youtube_url, output_path):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            print("No audio stream found.")
            return None
        audio_file = audio_stream.download(filename=output_path)
        return audio_file
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None

def extract_audio_from_video(video_path, audio_output_path):
    try:
        video_clip = mp.VideoFileClip(video_path)
        video_clip.audio.write_audiofile(audio_output_path)
    except Exception as e:
        print(f"Error extracting audio: {e}")

def convert_audio_to_text(audio_path):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    except Exception as e:
        print(f"Error converting audio to text: {e}")
        return ""



# Download YouTube video audio
video_file = download_youtube_audio(youtube_url, video_output_path)
if video_file:
    # Extract audio from video
    extract_audio_from_video(video_file, audio_output_path)

    # Convert audio to text
    text = convert_audio_to_text(audio_output_path)

    # Print the extracted text
    print("\nThe resultant text from the video is:\n")
    print(text)

    # Clean up temporary files
    os.remove(video_file)
    os.remove(audio_output_path)
else:
    print("Failed to download audio from YouTube.")
