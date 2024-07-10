from openai import OpenAI, RateLimitError
from os import environ
import backoff


class ConsultationService():
    @staticmethod
    @backoff.on_exception(backoff.expo, RateLimitError, max_time=60)
    def transcription(user_id, filepath):
        client = OpenAI(api_key = environ.get('OPENAI_API_KEY'))
        with open(filepath, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            return transcription.text