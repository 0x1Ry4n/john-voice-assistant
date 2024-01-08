# John Bot - Voice Assistant - Gesture Recognition

## Overview

The project utilizes machine learning algorithms and computer vision to recognize hand gestures and voice commands, functioning without additional hardware requirements. The frontend was developed using HTML, CSS, and JS and runs directly on localhost.

![ChatBot Image](https://ibb.co/jg9YnvN)

![Gesture Image](https://ibb.co/4mhRYz0)

## Technologies Used

- **Voice Recognition:** Voice recognition is performed through the "speech_recognition" package.

- **Gesture Recognition:** For gesture recognition, CNN models implemented by the "mediapipe" package were employed. The control of mouse cursor is improved by "pyautogui" library.

## Current Phase

The project is in its early stages, and some features have not been fully tested or refined yet, resulting in temporary solutions

## Execution Instructions

1. Clone the repository.
2. Setup the environment with python greather than the **3.8.5** version
3. Setup **OPEN_WEATHER_API_TOKEN** on .env file
4. Run the following commands:

```bash
$ conda create --name john-env python=3.8.5
$ conda activate john-env
$ pip install -r requirements.txt
$ python app.py
```

## Usage

1. Use 'john commands' to list all commands
2. Speak with the voice assistant to run the commands or type on input chatbot
