from django.urls import path
from .views import (
    translate_text,
    generate_sentences,
    speech_to_text,
    text_to_speech,
    check_pronunciation
)

urlpatterns = [
    path('translate/', translate_text, name='translate'),
    path('generate-sentences/', generate_sentences, name='generate_sentences'),
    path('speech-to-text/', speech_to_text, name='speech_to_text'),
    path('text-to-speech/', text_to_speech, name='text_to_speech'),
    path('pronunciation/', check_pronunciation, name='check_pronunciation'),
]
