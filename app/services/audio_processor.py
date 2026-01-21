# File: app/services/audio_processor.py
"""
Audio transcription service using faster-whisper (open source).
"""
import os
from typing import Dict, Any, List, Optional
from faster_whisper import WhisperModel
from pydub import AudioSegment

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("TAP.AudioProcessor")

# Global model instance (lazy loaded)
_whisper_model: Optional[WhisperModel] = None


def get_whisper_model() -> WhisperModel:
    """
    Get or create the Whisper model instance.
    Uses 'base' model by default for balance of speed and accuracy.
    """
    global _whisper_model
    
    if _whisper_model is None:
        logger.info("Loading Whisper model...")
        # Use 'base' for good balance, 'small' or 'medium' for better accuracy
        # 'large-v3' for best accuracy but slower
        _whisper_model = WhisperModel(
            "base",
            device="cpu",  # Use "cuda" if GPU available
            compute_type="int8"  # Quantized for faster CPU inference
        )
        logger.info("Whisper model loaded successfully.")
    
    return _whisper_model


def get_audio_duration(file_path: str) -> float:
    """
    Get the duration of an audio file in seconds.
    
    Args:
        file_path: Path to the audio file
    
    Returns:
        Duration in seconds
    """
    try:
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # Convert ms to seconds
    except Exception as e:
        logger.error(f"Error getting audio duration: {str(e)}")
        return 0.0


def convert_to_wav(input_path: str, output_path: str) -> str:
    """
    Convert audio file to WAV format for Whisper.
    
    Args:
        input_path: Path to input audio file
        output_path: Path for output WAV file
    
    Returns:
        Path to the WAV file
    """
    try:
        audio = AudioSegment.from_file(input_path)
        # Whisper works best with 16kHz mono audio
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        logger.error(f"Error converting audio: {str(e)}")
        raise


def transcribe_audio(file_path: str, language: str = "en") -> Dict[str, Any]:
    """
    Transcribe audio file using faster-whisper.
    
    Args:
        file_path: Path to the audio file
        language: Language code (default: 'en' for English)
    
    Returns:
        Dictionary with transcript and segments
    """
    try:
        logger.info(f"Starting transcription of: {file_path}")
        
        # Get the model
        model = get_whisper_model()
        
        # Get audio duration
        duration = get_audio_duration(file_path)
        logger.info(f"Audio duration: {duration:.2f} seconds")
        
        # Transcribe
        segments, info = model.transcribe(
            file_path,
            language=language,
            beam_size=5,
            word_timestamps=False,  # Set to True for word-level timestamps
            vad_filter=True,  # Voice activity detection
            vad_parameters=dict(min_silence_duration_ms=500),
        )
        
        # Process segments
        transcript_parts = []
        segment_list = []
        
        for segment in segments:
            transcript_parts.append(segment.text.strip())
            segment_list.append({
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip(),
            })
        
        full_transcript = " ".join(transcript_parts)
        
        logger.info(f"Transcription complete. Segments: {len(segment_list)}")
        
        return {
            "transcript": full_transcript,
            "segments": segment_list,
            "duration_seconds": duration,
            "language": info.language,
            "language_probability": round(info.language_probability, 3),
        }
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise


def format_transcript_with_timestamps(segments: List[Dict[str, Any]]) -> str:
    """
    Format transcript segments with timestamps for display.
    
    Args:
        segments: List of segment dictionaries with start, end, text
    
    Returns:
        Formatted transcript string
    """
    lines = []
    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        
        # Format as [MM:SS - MM:SS] text
        start_min, start_sec = divmod(int(start), 60)
        end_min, end_sec = divmod(int(end), 60)
        
        timestamp = f"[{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}]"
        lines.append(f"{timestamp} {text}")
    
    return "\n".join(lines)


def clean_transcript(text: str) -> str:
    """
    Clean up transcript text.
    
    - Remove excessive whitespace
    - Fix common transcription errors
    - Normalize punctuation
    """
    import re
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove filler words (common in transcriptions)
    filler_words = [" um ", " uh ", " like ", " you know "]
    for filler in filler_words:
        text = text.replace(filler, " ")
    
    # Normalize spaces around punctuation
    text = re.sub(r'\s+([.,!?])', r'\1', text)
    text = re.sub(r'([.,!?])(\w)', r'\1 \2', text)
    
    return text.strip()
