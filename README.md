
# 🎥 Video Summarization using AI

This project demonstrates **AI-powered video summarization**, where keyframes and textual summaries are extracted automatically from videos to generate concise representations. It uses computer vision and NLP techniques to process videos and highlight the most important scenes, enabling efficient content consumption and indexing.

<p align="center">
  <img src="https://github.com/Hina19/video-summarization-using-AI/raw/main/assets/demo.gif" alt="Demo GIF" width="600"/>
</p>

---

## 🚀 Key Features

✅ Extracts frames from input video  
✅ Generates video summary using AI techniques  
✅ Visualizes keyframes and generates textual summaries  
✅ Implemented in an easy-to-follow Jupyter notebook  
✅ Ready-to-run with example video  

---

## 🛠️ Technologies Used

- Python 3.x
- OpenCV
- NLTK
- NumPy
- Matplotlib
- Jupyter Notebook

---

## 📸 Demo Output

After running the notebook, you will get:
- Extracted keyframes saved as images
- A textual summary describing the video content

---

## 🏃‍♀️ How to Run

1️⃣ **Clone the repo:**
```bash
git clone https://github.com/Hina19/video-summarization-using-AI.git
cd video-summarization-using-AI
2️⃣ Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
(Create a requirements.txt if you haven’t already, for example:)

Copy
Edit
opencv-python
nltk
numpy
matplotlib
3️⃣ Download a sample video:

Place your video file in the project root or modify the notebook to point to your own video file.

4️⃣ Run the notebook:

bash
Copy
Edit
jupyter notebook Video-summarization.ipynb
📚 How it Works
Frame Extraction: The video is read frame by frame, and significant frames are selected based on scene changes.

Keyframe Selection: Frames are compared using color histogram differences.

Textual Summarization: Using NLP techniques to generate captions from frame information.

Visualization: Keyframes and summary text are displayed.

🌟 Use Cases
✅ Short-form previews for long videos
✅ Content indexing for search engines
✅ Educational video summarization
✅ Highlight reels for sports or events

🙌 Contributing
Feel free to fork this repo, raise issues, or submit pull requests! Contributions are welcome.
