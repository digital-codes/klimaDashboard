import { createApp, h, Fragment } from 'vue'
import App from './App.vue'

import router from '@/router';

/*
import "@fontsource/source-sans-pro"; // Defaults to weight 400
import "@fontsource/source-sans-pro/400.css"; // Specify weight
import "@fontsource/source-sans-pro/400-italic.css"; // Specify weight and style
*/

// include only latin ...
//import "@fontsource/roboto"; // Defaults to weight 400
//import "@fontsource/roboto/latin.css"; // Defaults to weight 400
//import "@fontsource/roboto-condensed/latin.css"; // Defaults to weight 400
// normally, we use only 400,500 and 700 weights
import "@fontsource/roboto/latin-400.css"; // Defaults to weight 400
import "@fontsource/roboto-condensed/latin-400.css"; // Defaults to weight 400
import "@fontsource/roboto/latin-500.css"; // Defaults to weight 400
import "@fontsource/roboto-condensed/latin-500.css"; // Defaults to weight 400
import "@fontsource/roboto/latin-700.css"; // Defaults to weight 400
import "@fontsource/roboto-condensed/latin-700.css"; // Defaults to weight 400


// https://www.npmjs.com/package/material-icons
// https://marella.me/material-icons/demo/
//import 'material-icons/iconfont/material-icons.css';
// import only used icons styles. NB: two-tone doesn't work with dark mode (by default)
import 'material-icons/iconfont/filled.css';
import 'material-icons/iconfont/outlined.css';


/* noto font and icons **
https://www.npmjs.com/package/@fontsource/noto-sans
https://www.npmjs.com/package/@fontsource/noto-color-emoji
*/
/*
import "@fontsource/noto-sans"; // Defaults to weight 400
import "@fontsource/noto-sans/400.css"; // Specify weight
import "@fontsource/noto-sans/400-italic.css"; // Specify weight and st

import "@fontsource/noto-color-emoji"; // Defaults to weight 400
import "@fontsource/noto-color-emoji/400.css"; // Specify weight
import "@fontsource/noto-color-emoji/400-italic.css"; // Specify weight and style
*/
// import "@fontsource/noto-sans/latin.css"; // Defaults to weight 400
import "@fontsource/noto-sans/latin-700.css"; // Used only in h2 with weigh 700
// noto emojis are very large, so use them only when needed
//import "@fontsource/noto-color-emoji/400.css";

/* use noto emojis like so:
<va-icon class="emoji"> &#x1F600; Click me! &#x1F389;</va-icon>
.emoji {
  font-family: 'Noto Color Emoji';
  font-size: 1.5rem!important;
  font-weight:400;
}
*/

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

// Set lang attribute dynamically
document.documentElement.lang = i18n.global.locale.value;


// pinia 
//import { useStore } from 'pinia';
//const configStore = useStore('configStore'); // Replace 'configStore' with the name of your specific store
import { createPinia } from 'pinia'
const pinia = createPinia()

const app = createApp(App)
app.use(pinia)
app.use(i18n)
app.use(router);
app.use(
    createVuestic(
        {
            config: {
                colors: {
                    presets: {
                        light: {
                            primary: "#048500",
                        },
                        dark: {
                            primary: "#048500",
                        },
                    },
                },
            },
        }
    )
)
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




