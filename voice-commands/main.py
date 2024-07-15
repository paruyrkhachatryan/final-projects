import speech_recognition as sr
import subprocess

def recognize_speech():
    """
    Capture speech from the microphone and recognize it using Google Speech Recognition.

    This function uses the SpeechRecognition library to capture audio from the default
    microphone and then attempts to recognize the speech using the Google Web Speech API.
    If the recognition is successful, it returns the recognized text in lowercase. If there
    is an error, it prints an appropriate message and returns None.

    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language='en-US')
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    
    return None


def execute_command(command):
    """

    This function takes a recognized speech command as input and executes the corresponding
    system command. The supported commands include listing files, opening applications like
    Google Chrome and Notepad, and opening specific websites like YouTube, Facebook, Twitter,
    and Instagram. If the command is not recognized, it prints a message indicating.

    
    """
    if "list files" in command:
        subprocess.run("dir", shell=True, check=True)
    elif "open google chrome" in command:
        subprocess.run("start chrome", shell=True, check=True)
    elif "open notepad" in command:
        subprocess.run("notepad", shell=True, check=True)
    elif "open youtube" in command:
        subprocess.run("start https://www.youtube.com", shell=True, check=True)
    elif "open facebook" in command:
        subprocess.run("start https://www.facebook.com", shell=True, check=True)
    elif "open twitter" in command:
        subprocess.run("start https://www.twitter.com", shell=True, check=True)
    elif "open instagram" in command:
        subprocess.run("start https://www.instagram.com", shell=True, check=True)
    else:
        print("Command not recognized.")


if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if command:
            execute_command(command)
