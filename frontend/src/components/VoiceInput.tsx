import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './VoiceInput.module.css';

type VoiceInputProps = {
  onTranscript: (transcript: string) => void;
  onError?: (error: string) => void;
  className?: string;
};

const VoiceInput: React.FC<VoiceInputProps> = ({
  onTranscript,
  onError,
  className
}) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isSupported, setIsSupported] = useState(true);

  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsSupported(false);
      if (onError) {
        onError('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
      }
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event: any) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      const combinedTranscript = finalTranscript + interimTranscript;
      setTranscript(combinedTranscript);

      if (finalTranscript) {
        onTranscript(finalTranscript);
        stopListening();
      }
    };

    recognition.onerror = (event: any) => {
      if (onError) {
        onError(`Speech recognition error: ${event.error}`);
      }
      stopListening();
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [onTranscript, onError]);

  const startListening = () => {
    if (!isSupported) return;

    try {
      recognitionRef.current.start();
      setIsListening(true);
      setTranscript('');
    } catch (error) {
      if (onError) {
        onError('Failed to start speech recognition. Please check microphone permissions.');
      }
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  if (!isSupported) {
    return (
      <div className={clsx(styles.unsupported, className)}>
        Voice input is not supported in this browser. Please use Chrome or Edge.
      </div>
    );
  }

  return (
    <div className={clsx(styles.voiceInput, className)}>
      <button
        className={clsx(
          styles.voiceButton,
          isListening && styles.listening
        )}
        onClick={isListening ? stopListening : startListening}
        aria-label={isListening ? 'Stop listening' : 'Start voice input'}
        title={isListening ? 'Click to stop listening' : 'Click to start voice input'}
      >
        {isListening ? (
          <>
            <div className={styles.recordingIndicator}></div>
            <span>Recording...</span>
          </>
        ) : (
          <>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className={styles.micIcon}
            >
              <path d="M5.037 7.037A7.5 7.5 0 0 1 12 3c1.86 0 3.573.616 4.963 1.634M12 3v18a2.25 2.25 0 0 1-2.25-2.25h4.5A2.25 2.25 0 0 1 16.5 21V3a9 9 0 0 0-9 9c0 1.98.617 3.693 1.634 4.963M12 3a9 9 0 0 1 9 9c0 1.98-.617 3.693-1.634 4.963" />
            </svg>
            <span>Voice Input</span>
          </>
        )}
      </button>

      {transcript && (
        <div className={styles.transcript}>
          <p>{transcript}</p>
        </div>
      )}
    </div>
  );
};

export default VoiceInput;