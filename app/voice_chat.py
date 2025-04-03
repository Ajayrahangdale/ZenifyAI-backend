import speech_recognition as sr
import pyttsx3

# Initialize speech engine
engine = pyttsx3.init()

# Set properties for better speech clarity
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to listen to user's voice and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Set limits
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio")
            return "Sorry, I did not understand"
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return "Sorry, I could not process your request"
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected")
            return "No speech detected"

# Example usage
if __name__ == "__main__":
    speak("Hello! I am listening to you.")
    user_input = listen()
    speak(f"You said: {user_input}")
