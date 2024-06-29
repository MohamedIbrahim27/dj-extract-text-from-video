import moviepy.editor as mp
import os
import speech_recognition as sr

def extract_audio_from_video(video_path, output_dir):
    try:
        # Load video file
        clip = mp.VideoFileClip(video_path)
        duration = clip.duration
        print(f"The video is {duration} seconds")

        # Extract audio
        audio_filename = os.path.join(output_dir, 'audio.wav')
        clip.audio.write_audiofile(audio_filename, buffersize=200000)

        # Convert audio to text
        text = convert_audio_to_text(audio_filename)
        print(f"Extracted text: {text}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        print(f"An error occurred during audio to text conversion: {str(e)}")
        return ""

if __name__ == "__main__":
    video_path = "WhatsApp Video 2024-06-27 at 07.01.49_67b78ae5.mp4"
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    extract_audio_from_video(video_path, output_dir)
