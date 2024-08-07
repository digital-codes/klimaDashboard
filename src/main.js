import { createApp } from 'vue'
import App from './App.vue'

import router from '@/router';

/*
import "@fontsource/source-sans-pro"; // Defaults to weight 400
import "@fontsource/source-sans-pro/400.css"; // Specify weight
import "@fontsource/source-sans-pro/400-italic.css"; // Specify weight and style
*/

// include only latin ...
//import "@fontsource/roboto"; // Defaults to weight 400
import "@fontsource/roboto/latin.css"; // Defaults to weight 400

// https://www.npmjs.com/package/material-icons
// https://marella.me/material-icons/demo/
//import 'material-icons/iconfont/material-icons.css';
// import only used icons styles. NB: two-tone doesn't work with dark mode (by default)
import 'material-icons/iconfont/filled.css';
import 'material-icons/iconfont/outlined.css';


import { createVuestic } from "vuestic-ui";
import "vuestic-ui/css";

// after vuestic-css
import './style/style.scss'

// internationalization
const defaultLocale = "de"
// globals messages and for App.vue, apart from sidebar
import messages from '@/locales/lang.json';
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
app.use(pinia)
app.use(i18n)
app.use(router);
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




