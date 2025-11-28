# app/services/azure_tts.py

import azure.cognitiveservices.speech as speechsdk
from fastapi import HTTPException
from app.core.config import settings


class AzureTTSService:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=settings.AZURE_TTS_KEY,
            region=settings.AZURE_TTS_REGION,
        )
        self.speech_config.speech_synthesis_voice_name = settings.AZURE_TTS_VOICE

        # Standard WAV format (16kHz 16-bit mono PCM)
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )

    def text_to_speech(self, text: str) -> bytes:
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Empty text for TTS")

        # Create PullAudioOutputStream for in-memory buffering
        pull_stream = speechsdk.audio.PullAudioOutputStream()

        # Route synthesis output to the stream
        audio_config = speechsdk.audio.AudioOutputConfig(stream=pull_stream)

        # 👈 FIX: No 'with' — just create normally (SDK doesn't support context manager)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config,
        )

        try:
            # Synthesize (blocks until complete)
            result = synthesizer.speak_text_async(text).get()

            print(f">>> TTS Result reason: {result.reason}")
            print(f">>> Text sample (first 100 chars): {text[:100]}...")

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                # Flush any remaining data
                synthesizer.stop_speaking()

                # Chunked read loop with silence detection (from your working logs)
                chunk_size = 4096
                chunks = []
                total_bytes = 0
                silence_chunks = 0
                max_silence_chunks = 5  # Stop after 5 full zero-chunks

                while True:
                    audio_buffer = bytes(chunk_size)
                    filled_size = pull_stream.read(audio_buffer)

                    if filled_size == 0:
                        print(">>> Stream ended cleanly (filled_size == 0)")
                        break

                    # Detect trailing silence (all zeros) – Azure's padding
                    if filled_size == chunk_size and all(b == 0 for b in audio_buffer):
                        silence_chunks += 1
                        print(f">>> Detected silence chunk #{silence_chunks}")
                        if silence_chunks >= max_silence_chunks:
                            print(">>> Stopping: too many silence chunks (end of real audio)")
                            break
                    else:
                        # Real audio data — reset silence counter
                        silence_chunks = 0

                    chunks.append(audio_buffer[:filled_size])
                    total_bytes += filled_size

                    # Safety: Cap at 2MB
                    if total_bytes > 2_000_000:
                        print(">>> Emergency break: audio too large")
                        break

                audio_bytes = b"".join(chunks)
                print(f">>> FINAL AUDIO SIZE: {len(audio_bytes)} bytes")

                if not audio_bytes:
                    raise HTTPException(
                        status_code=500,
                        detail="Azure TTS returned empty audio data",
                    )

                return audio_bytes

            elif result.reason == speechsdk.ResultReason.Canceled:
                details = result.cancellation_details
                raise HTTPException(
                    status_code=500,
                    detail=f"Azure TTS canceled: {details.reason} - {details.error_details}",
                )

            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Azure TTS failed with reason: {result.reason}",
                )

        finally:
            # 👈 Always clean up: Stop and let GC handle the rest (no explicit close needed)
            synthesizer.stop_speaking()
            # No pull_stream.close() — not available; GC will handle