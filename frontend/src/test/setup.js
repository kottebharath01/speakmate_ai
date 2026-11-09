import '@testing-library/jest-dom';

// Mock Web Speech API SpeechSynthesis
window.speechSynthesis = {
  speak: () => {},
  cancel: () => {},
  getVoices: () => [],
  onvoiceschanged: null,
};

// Mock SpeechRecognition
window.SpeechRecognition = class {
  constructor() {
    this.continuous = false;
    this.interimResults = false;
    this.lang = 'en-US';
  }
  start() {}
  stop() {}
  abort() {}
};
window.webkitSpeechRecognition = window.SpeechRecognition;
