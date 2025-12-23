from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tempfile
import os

from .services import (
    AITranslator,
    SentenceGenerator,
    GermanTutor,
    SpeechService,
    PronunciationChecker
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_text(request):
    """
    Translate text with grammar explanation.
    
    POST data:
        text: Text to translate
        source_lang: Source language (de, en, ar)
        target_lang: Target language (de, en, ar)
    """
    
    text = request.data.get('text', '')
    source_lang = request.data.get('source_lang', 'de')
    target_lang = request.data.get('target_lang', 'en')
    
    if not text:
        return Response(
            {'error': 'Text is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    result = AITranslator.translate(text, source_lang, target_lang)
    
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_sentences(request):
    """
    Generate example sentences for a word.
    
    POST data:
        word: German word
        level: Language level (A1, A2, etc.)
        count: Number of sentences (default: 3)
    """
    
    word = request.data.get('word', '')
    level = request.data.get('level', request.user.language_level)
    count = request.data.get('count', 3)
    
    if not word:
        return Response(
            {'error': 'Word is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    sentences = SentenceGenerator.generate_sentences(word, level, count)
    
    return Response({'sentences': sentences})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def speech_to_text(request):
    """
    Convert speech to text.
    
    POST data:
        audio: Audio file
    """
    
    audio_file = request.FILES.get('audio')
    
    if not audio_file:
        return Response(
            {'error': 'Audio file is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)
        temp_path = temp_file.name
    
    try:
        with open(temp_path, 'rb') as audio:
            result = SpeechService.speech_to_text(audio)
        
        return Response(result)
    
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def text_to_speech(request):
    """
    Convert text to speech.
    
    POST data:
        text: German text
        speed: Speech speed (0.5 to 2.0, default: 1.0)
    """
    
    text = request.data.get('text', '')
    speed = float(request.data.get('speed', 1.0))
    
    if not text:
        return Response(
            {'error': 'Text is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    audio_content = SpeechService.text_to_speech(text, speed)
    
    if not audio_content:
        return Response(
            {'error': 'Failed to generate speech'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Save audio file
    filename = f'tts_{request.user.id}_{hash(text)}.mp3'
    path = default_storage.save(f'audio/{filename}', ContentFile(audio_content))
    
    return Response({
        'audio_url': default_storage.url(path),
        'success': True
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_pronunciation(request):
    """
    Check pronunciation accuracy.
    
    POST data:
        expected_text: What should be said
        audio: Audio file of user speaking
    """
    
    expected_text = request.data.get('expected_text', '')
    audio_file = request.FILES.get('audio')
    
    if not expected_text or not audio_file:
        return Response(
            {'error': 'Expected text and audio file are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Convert speech to text
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)
        temp_path = temp_file.name
    
    try:
        with open(temp_path, 'rb') as audio:
            transcription = SpeechService.speech_to_text(audio)
        
        if not transcription['success']:
            return Response(
                {'error': 'Failed to transcribe audio'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        spoken_text = transcription['text']
        result = PronunciationChecker.check_pronunciation(expected_text, spoken_text)
        
        return Response(result)
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
