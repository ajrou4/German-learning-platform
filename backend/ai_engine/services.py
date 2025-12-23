"""
AI Engine services for German learning platform.
Integrates Google Gemini API for AI-powered features.
"""

import google.generativeai as genai
from django.conf import settings
from typing import Dict, List, Optional
import json

# Configure Gemini API
genai.configure(api_key=settings.GOOGLE_API_KEY)


class AITranslator:
    """AI-powered translation service with grammar explanations."""
    
    @staticmethod
    def translate(
        text: str,
        source_lang: str = 'de',
        target_lang: str = 'en'
    ) -> Dict:
        """
        Translate text and provide grammar breakdown.
        
        Args:
            text: Text to translate
            source_lang: Source language code (de, en, ar)
            target_lang: Target language code (de, en, ar)
        
        Returns:
            Dict with translation, grammar explanation, and word breakdown
        """
        
        lang_names = {
            'de': 'German',
            'en': 'English',
            'ar': 'Arabic'
        }
        
        prompt = f"""Translate the following {lang_names.get(source_lang, 'German')} text to {lang_names.get(target_lang, 'English')} and provide:
1. Translation
2. Grammar explanation
3. Word breakdown

Text: {text}

Format your response as JSON:
{{
    "translation": "...",
    "grammar_explanation": "...",
    "word_breakdown": [
        {{"word": "...", "meaning": "...", "grammar_note": "..."}}
    ]
}}"""
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            return result
            
        except Exception as e:
            return {
                "translation": f"Error: {str(e)}",
                "grammar_explanation": "",
                "word_breakdown": []
            }


class SentenceGenerator:
    """Generate example sentences for vocabulary words."""
    
    @staticmethod
    def generate_sentences(word: str, level: str = 'A1', count: int = 3) -> List[Dict]:
        """
        Generate example sentences for a German word.
        
        Args:
            word: German word
            level: Language level (A1, A2, B1, etc.)
            count: Number of sentences to generate
        
        Returns:
            List of dicts with German sentence and English translation
        """
        
        prompt = f"""Generate {count} example sentences using the German word "{word}" suitable for {level} level learners.
Include one real-life practical example.

Format as JSON:
{{
    "sentences": [
        {{"german": "...", "english": "...", "context": "..."}}
    ]
}}"""
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            return result.get('sentences', [])
            
        except Exception as e:
            return [{"german": f"Error: {str(e)}", "english": "", "context": ""}]


class GermanTutor:
    """AI chatbot for German learning assistance."""
    
    @staticmethod
    def chat(
        message: str,
        conversation_history: List[Dict],
        mode: str = 'beginner',
        user_level: str = 'A1'
    ) -> str:
        """
        Chat with AI German tutor.
        
        Args:
            message: User's message
            conversation_history: Previous messages
            mode: Chat mode (beginner, grammar, conversation)
            user_level: User's language level
        
        Returns:
            AI tutor's response
        """
        
        system_prompts = {
            'beginner': f"""You are a friendly German language tutor for {user_level} level students.
- Use simple German with English explanations
- Correct mistakes politely
- Encourage the learner
- Keep responses concise""",
            
            'grammar': f"""You are a German grammar expert for {user_level} level students.
- Explain grammar rules clearly
- Provide examples
- Use tables and structured explanations
- Reference common mistakes""",
            
            'conversation': f"""You are a German conversation partner for {user_level} level students.
- Respond naturally in German
- Gently correct mistakes
- Ask follow-up questions
- Keep the conversation flowing"""
        }
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Build conversation context
            system_prompt = system_prompts.get(mode, system_prompts['beginner'])
            
            # Combine system prompt with conversation history
            full_prompt = f"{system_prompt}\n\n"
            
            # Add conversation history (last 10 messages)
            for msg in conversation_history[-10:]:
                role = "User" if msg['role'] == 'user' else "Assistant"
                full_prompt += f"{role}: {msg['content']}\n"
            
            # Add current message
            full_prompt += f"User: {message}\nAssistant:"
            
            response = model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"


class SpeechService:
    """Speech-to-text and text-to-speech services."""
    
    @staticmethod
    def speech_to_text(audio_file) -> Dict:
        """
        Convert speech to text using Whisper.
        
        Args:
            audio_file: Audio file object
        
        Returns:
            Dict with transcription and confidence
        """
        
        # Note: Gemini API doesn't provide speech-to-text yet
        # This would require Google Cloud Speech-to-Text API
        return {
            "text": "",
            "success": False,
            "error": "Speech-to-text is not yet implemented. Please use Google Cloud Speech-to-Text API for this feature."
        }
    
    @staticmethod
    def text_to_speech(text: str, speed: float = 1.0) -> bytes:
        """
        Convert text to speech.
        
        Args:
            text: German text to convert
            speed: Speech speed (0.5 to 2.0)
        
        Returns:
            Audio bytes
        """
        
        # Note: Gemini API doesn't provide text-to-speech yet
        # This would require Google Cloud Text-to-Speech API
        return b""


class PronunciationChecker:
    """Check pronunciation accuracy."""
    
    @staticmethod
    def check_pronunciation(
        expected_text: str,
        spoken_text: str
    ) -> Dict:
        """
        Compare expected text with spoken text.
        
        Args:
            expected_text: What should have been said
            spoken_text: What was actually said
        
        Returns:
            Dict with accuracy score and feedback
        """
        
        # Simple word-by-word comparison
        expected_words = expected_text.lower().split()
        spoken_words = spoken_text.lower().split()
        
        correct_words = sum(1 for e, s in zip(expected_words, spoken_words) if e == s)
        total_words = max(len(expected_words), len(spoken_words))
        
        accuracy = (correct_words / total_words * 100) if total_words > 0 else 0
        
        feedback = "Excellent!" if accuracy >= 90 else \
                   "Good job!" if accuracy >= 70 else \
                   "Keep practicing!" if accuracy >= 50 else \
                   "Try again!"
        
        return {
            "accuracy": round(accuracy, 2),
            "feedback": feedback,
            "expected": expected_text,
            "spoken": spoken_text,
            "correct_words": correct_words,
            "total_words": total_words
        }
