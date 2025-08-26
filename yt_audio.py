import yt_dlp
import os
from pydub import AudioSegment
import speech_recognition as sr
from transformers import pipeline

# Function to download YouTube video and extract audio
def download_audio_from_youtube(url):
    # Set up the YouTube download options
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,  # Only download audio
        'audioquality': 1,  # Best audio quality
        'outtmpl': 'downloaded_audio.%(ext)s',  # Output file name template
    }

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = info_dict['title'] + '.webm'
        print(f"Downloaded audio file: {audio_file}")
        return audio_file

# Function to convert audio file (e.g., .webm) to .wav
def convert_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    audio.export("audio.wav", format="wav")
    print("Converted to .wav")
    return "audio.wav"

# Function to transcribe audio to text
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    
    try:
        print("Transcribing audio...")
        text = recognizer.recognize_google(audio_data)
        print("Transcription successful.")
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError as e:
        return f"Error with the speech recognition service: {e}"

# Function to summarize the text
def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Main function to execute the process
def main(url):
    # Step 1: Download audio from YouTube
    audio_file = download_audio_from_youtube(url)

    # Step 2: Convert audio to wav format (if not already in wav)
    audio_path = convert_to_wav(audio_file)

    # Step 3: Transcribe the audio to text
    transcribed_text = transcribe_audio(audio_path)

    # Step 4: Summarize the transcribed text
    summary = summarize_text(transcribed_text)

    # Print the results
    print("\nOriginal Transcript:")
    print(transcribed_text[:500])  # Display the first 500 characters
    print("\nSummary:")
    print(summary)

    # Clean up downloaded files
    os.remove(audio_file)
    os.remove(audio_path)

# Example: Replace with any YouTube video URL
video_url = "https://www.youtube.com/watch?v=your_video_id_here"
main(video_url)
