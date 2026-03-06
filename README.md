# Jarvis AI Voice Assistant

Jarvis is a Python-based voice assistant that can execute commands, retrieve information, and interact with AI models using voice input.

## Features

- Voice activation using speech recognition
- AI-generated responses using OpenAI
- YouTube video search and playback
- Latest news retrieval
- Screenshot automation
- Browser automation
- Text-to-speech voice responses
- Custom deep male voice using Piper TTS

## Technologies Used

- Python
- OpenAI API
- SpeechRecognition
- PyAutoGUI
- Pygame
- Requests
- gTTS

## Project Structure

```
jarvis-ai-assistant/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── voices/
│   ├── alan-medium.onnx
│   └── alan-medium.onnx.json
```

## Installation

1. Clone the repository

```
git clone https://github.com/yourusername/jarvis-ai-assistant.git
```

2. Navigate into the project folder

```
cd jarvis-ai-assistant
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Create a `.env` file and add your API keys

Example:

```
OPENAI_API_KEY=your_api_key_here
NEWS_API_KEY=your_news_api_key
GOOGLE_API_KEY=your_google_api_key
```

5. Run the project

```
python main.py
```

## Demo

Example interaction with the Jarvis assistant:

![Jarvis Demo](assets/demo.png)

## Author

Mohammed Tayubudeen R