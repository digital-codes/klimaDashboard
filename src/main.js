import { createApp } from 'vue'
import App from './App.vue'

import router from '@/router';

/*
import "@fontsource/source-sans-pro"; // Defaults to weight 400
import "@fontsource/source-sans-pro/400.css"; // Specify weight
import "@fontsource/source-sans-pro/400-italic.css"; // Specify weight and style
*/

import "@fontsource/roboto"; // Defaults to weight 400
//import "@fontsource/roboto/400.css"; // Specify weight
//import "@fontsource/roboto/400-italic.css"; // Specify weight and style

// https://www.npmjs.com/package/material-icons
import 'material-icons/iconfont/material-icons.css';


import { createVuestic } from "vuestic-ui";
import "vuestic-ui/css";

// after vuestic-css
import './style/style.scss'

// internationalization
const defaultLocale = "de"
import messages from '@/locales/messages.json';
import { createI18n } from 'vue-i18n';
const i18n = createI18n({
    legacy: false,
    locale: defaultLocale,
    messages: {
        ...messages
    },
});

// pinia 
//import { useStore } from 'pinia';
//const configStore = useStore('configStore'); // Replace 'configStore' with the name of your specific store
import { createPinia } from 'pinia'
const pinia = createPinia()

const app = createApp(App)
app.use(router);
app.use(pinia)
app.use(i18n)
app.use(createVuestic())
app.mount('#app')

import { useConfigStore } from '@/services/configStore'; // Replace 'configStore' with the name of your specific store
const configStore = useConfigStore()
configStore.setCurrentLocale(defaultLocale)
configStore.setMessages(messages)

/*
console.log("configStore", configStore)
console.log("configStore", configStore.locale)
console.log("configStore", configStore.messages)

console.log("configStore.getCurrentLocale():", configStore.getCurrentLocale)
console.log("configStore.getMessages():", configStore.getMessages)
*/




