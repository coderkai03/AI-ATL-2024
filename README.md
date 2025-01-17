# InstaRizz

InstaRizz is a real-time, wearable-powered social assistant that captures live video from Ray-Ban smart glasses, identifies individuals, and generates personalized bios and pickup lines in real-time through a custom AI pipeline. This project was built for a hackathon to explore the intersection of AI, social interaction, and wearable technology.

## 🚀 Features

- **Live Video Streaming**: Streams live video from Ray-Ban smart glasses directly to Instagram Live.
- **Real-Time Facial Recognition**: Captures frames from the live stream and identifies individuals using OpenCV.
- **Custom Identity Search**: Runs a custom classifier on our database to identify individuals based on their facial data.
- **AI-Generated Insights**: Uses Magic Loops API and GPT-4 to create a short bio and generate three pickup lines, displaying them instantly for the user.

## 🛠 Tech Stack

- **Ray-Ban Smart Glasses**: Wearable hardware for capturing video and live streaming.
- **OpenCV**: Used for real-time facial recognition on captured video frames.
- **Magic Loops**: Hosts a custom API pipeline for performing perplexity search to gather data on individuals and integrates with GPT-4.
- **GPT-4 API**: Generates bios and pickup lines based on individual data retrieved by Magic Loops.
- **Streamlit**: Provides a quick and interactive UI for showcasing InstaRizz's functionalities, including real-time data display.

## 📦 Setup

1. Clone the Repository:

   ```
   git clone https://github.com/username/InstaRizz.git
   cd InstaRizz
   ```
2. Install Dependencies:

   - Python 3.8+
   - Install required packages:
     ```
     pip install -r requirements.txt
     ```
3. Configure API Keys:

   - Set up environment variables for Magic Loops, GPT-4, and any other required API keys:
     ```
     export MAGIC_LOOPS_API_KEY='your_magic_loops_api_key'
     export GPT4_API_KEY='your_gpt4_api_key'
     ```
4. Run the Application:

   ```
   streamlit run app.py
   ```

## 🚧 Challenges & Solutions

- **Latency in Real-Time Processing**: We optimized snapshot intervals and OpenCV processing to handle data faster.
- **Privacy Considerations**: Ensured ethical use by focusing on public data and limiting private info retrieval.

## 🤔 Lessons Learned

InstaRizz taught us the importance of optimizing real-time data, managing privacy in AI-driven applications, and finding the right balance between speed and accuracy for social tech.

## 📅 Future Plans

- **Enhanced Privacy Controls**: Add more filters for ethical usage and data transparency.
- **Partnership with Instagram**: Explore a dedicated InstaRizz feed for richer user interactions.

## 📜 License

MIT License

InstaRizz is a playful step into AI-driven social engagement, blending real-time tech with personalization. Contributions and feedback are welcome!
