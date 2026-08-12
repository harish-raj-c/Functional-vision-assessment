export class VoiceRecognition {
  private recognition: any = null;
  private isListening = false;
  private onResult: ((transcript: string) => void) | null = null;

  constructor() {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      this.recognition = new (window as any).webkitSpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';

      this.recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        if (this.onResult) {
          this.onResult(transcript);
        }
      };

      this.recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        this.isListening = false;
      };

      this.recognition.onend = () => {
        this.isListening = false;
      };
    }
  }

  isSupported(): boolean {
    return this.recognition !== null;
  }

  start(callback: (transcript: string) => void) {
    if (!this.recognition) {
      console.warn('Speech recognition not supported');
      return;
    }

    this.onResult = callback;
    this.isListening = true;
    this.recognition.start();
  }

  stop() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    }
  }

  extractNumber(transcript: string): number | null {
    const numberWords: Record<string, number> = {
      'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
      'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
      'ten': 10
    };

    const lowerTranscript = transcript.toLowerCase().trim();
    
    // Check for number words
    if (numberWords[lowerTranscript] !== undefined) {
      return numberWords[lowerTranscript];
    }

    // Check for digit strings
    const match = lowerTranscript.match(/\d+/);
    if (match) {
      return parseInt(match[0], 10);
    }

    return null;
  }
}

export const voiceRecognition = new VoiceRecognition();
