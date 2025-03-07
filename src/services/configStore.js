import { defineStore } from 'pinia';

// update for pinia 3. store name is now a string
// https://pinia.vuejs.org/cookbook/migration-v2-v3.html

export const useConfigStore = defineStore('config', {
    state: () => ({
        locale: 'de', // default locale
        languages: [], // supported languages
        // add other config values here
        theme: "light",
        messages: {}

    }),
    getters: {
        getTheme() {
            return this.theme;
        },
        getCurrentLocale() {
            return this.locale;
        },
        // add other getters here
        getMessages() {
            return this.messages;
        },
        getLanguages() {
            return this.languages;
        }
    },
    actions: {
        setLanguages(languages) {
            this.languages = languages;
        },
        setTheme(theme) {
            this.theme = theme;
        },
        setCurrentLocale(locale) {
            this.locale = locale;
        },
        // add other actions here
        setMessages(messages) {
            this.messages = messages;
        }
    },
});
