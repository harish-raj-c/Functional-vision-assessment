export class KeyboardInput {
  private onKeyDown: ((key: string) => void) | null = null;

  constructor() {
    if (typeof window !== 'undefined') {
      window.addEventListener('keydown', this.handleKeyDown.bind(this));
    }
  }

  private handleKeyDown(event: KeyboardEvent) {
    if (this.onKeyDown) {
      this.onKeyDown(event.key);
    }
  }

  setCallback(callback: (key: string) => void) {
    this.onKeyDown = callback;
  }

  removeCallback() {
    this.onKeyDown = null;
  }

  extractNumber(key: string): number | null {
    if (key >= '0' && key <= '9') {
      return parseInt(key, 10);
    }
    return null;
  }

  destroy() {
    if (typeof window !== 'undefined') {
      window.removeEventListener('keydown', this.handleKeyDown.bind(this));
    }
    this.onKeyDown = null;
  }
}

export const keyboardInput = new KeyboardInput();
