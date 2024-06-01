import { createApp } from 'vue'

import "@fontsource/source-sans-pro"; // Defaults to weight 400
import "@fontsource/source-sans-pro/400.css"; // Specify weight
import "@fontsource/source-sans-pro/400-italic.css"; // Specify weight and style

// https://www.npmjs.com/package/material-icons
import 'material-icons/iconfont/material-icons.css';

import './style/style.css'


import { createVuestic } from "vuestic-ui";
import "vuestic-ui/css";


import App from './App.vue'

const app = createApp(App)
app.use(createVuestic())
app.mount('#app')
