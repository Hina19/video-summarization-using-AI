import streamlit as st
import os
import cv2
import torch
import moviepy.editor as mp
from PIL import Image
from gtts import gTTS
from scenedetect import open_video, SceneManager, ContentDetector
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoModelForCausalLM, AutoTokenizer
from openai import OpenAI
# Load AI models
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
client = OpenAI(
  api_key="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"
)


# Streamlit App UI
st.title("🎥 AI-Powered Video Summarization")

uploaded_file = st.file_uploader("📤 Upload a Video File", type=["mp4"])

if uploaded_file:
    video_path = "input_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.video(video_path)

    # Scene Detection & Frame Extraction
    st.write("🔍 Detecting scene changes and extracting key frames...")

    def extract_key_frames(video_path, output_folder="frames", frames_per_scene=3):
        os.makedirs(output_folder, exist_ok=True)
        video = open_video(video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=27.0))
        video.set_downscale_factor()
        scene_manager.detect_scenes(video)
        scenes = scene_manager.get_scene_list()
        cap = cv2.VideoCapture(video_path)
        for i, (start, end) in enumerate(scenes):
            start_frame = start.get_frames()
            end_frame = end.get_frames()
            step = (end_frame - start_frame) // (frames_per_scene + 1)
            for j in range(frames_per_scene):
                frame_time = start_frame + step * (j + 1)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_time)
                ret, frame = cap.read()
                if ret:
                    frame_path = os.path.join(output_folder, f"scene_{i+1}_frame{j+1}.jpg")
                    cv2.imwrite(frame_path, frame)
        cap.release()

    extract_key_frames(video_path)

    # Caption Generation
    st.write("📝 Generating captions for extracted frames...")

    def generate_caption(image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = caption_processor(image, return_tensors="pt")
        caption_ids = caption_model.generate(**inputs)
        return caption_processor.decode(caption_ids[0], skip_special_tokens=True)

    captions = []
    for filename in sorted(os.listdir("frames")):
        if filename.endswith(".jpg"):
            image_path = os.path.join("frames", filename)
            captions.append(generate_caption(image_path))

    st.write("📄 Generated Captions:", captions)

    # Summarization
    st.write("📖 Summarizing captions using AI...")

    def summarize_captions(captions):
      prompt = f"Summarize the following sequence of video frames into a meaningful story:\n\n{captions}"
      
      completion = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[{"role": "system", "content": "You are an AI that summarizes video content."},
                    {"role": "user", "content": prompt}]
      )
      return completion.choices[0].message.content
        

    summary = summarize_captions(captions)
    st.write("📌 Video Summary:", summary)

    # Text-to-Speech
    st.write("🔊 Generating voice narration...")

    def text_to_speech(text, output_audio="summary_audio.mp3"):
        tts = gTTS(text, lang="en")
        tts.save(output_audio)
    
    text_to_speech(summary)

    # Combine Audio & Video
    st.write("🎬 Merging audio with the video...")

    def add_audio_to_video(video_path, audio_path, output_video="final_video.mp4"):
        video = mp.VideoFileClip(video_path)
        audio = mp.AudioFileClip(audio_path)
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)
        final_video = video.set_audio(audio)
        final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")

    add_audio_to_video(video_path, "summary_audio.mp3")

    st.video("final_video.mp4")
