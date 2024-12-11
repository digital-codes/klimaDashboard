import { createI18n } from 'vue-i18n';

export const i18n = createI18n({
  legacy: false, // Use Composition API style
  locale: 'en', // Default locale
  globalInjection: true, // Makes $t and $d globally available
  messages: {
    en: {
      hello: 'Hello World',
      continue: 'Continue'
    },
    de: {
      hello: 'Hallo Welt',
      continue: 'Fortsetzen'
    }
  }
});

