// Polyfill for matchMedia and other browser APIs for Vitest
import '@testing-library/jest-dom';
if (typeof window !== 'undefined') {
  window.matchMedia = window.matchMedia || function() {
    return {
      matches: false,
      addListener: function() {},
      removeListener: function() {}
    };
  };
}
