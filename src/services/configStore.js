import { defineStore } from 'pinia';

export const useConfigStore = defineStore({
    id: 'config',
    state: () => ({
        locale: 'de', // default locale
        // add other config values here
        messages: {}
    }),
    getters: {
        getCurrentLocale() {
            return this.locale;
        },
        // add other getters here
        getMessages() {
            return this.messages;
        }
    },
    actions: {
        setCurrentLocale(locale) {
            this.locale = locale;
            console.log("setCurrentLocale", locale);
        },
        // add other actions here
        setMessages(messages) {
            this.messages = messages;
        }
    },
});
