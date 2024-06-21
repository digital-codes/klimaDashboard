import { defineStore } from 'pinia';

export const useConfigStore = defineStore({
    id: 'config',
    state: () => ({
        locale: 'de', // default locale
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
        }
    },
    actions: {
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
