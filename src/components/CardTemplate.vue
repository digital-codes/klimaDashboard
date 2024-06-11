<template>
    <div class="card">
        <p>{{ $t('hello') }}</p>
        <div class="header">{{ $t('header') }}</div>
        <div class="text">{{ $t('text') }}</div>
        <img :src="image" alt="Card Image" class="image" />
        <div class="chart-area">
            <!-- Chart component goes here -->
            <SizeAnimation></SizeAnimation>

        </div>
        <button class="button">{{ $t('button') }}</button>
        <input type="checkbox" class="checkbox" />
        <select class="select">
            <option value="option1">{{ $t('option1') }}</option>
            <option value="option2">{{ $t('option2') }}</option>
            <option value="option3">{{ $t('option3') }}</option>
        </select>
    </div>
</template>

<script setup>

import SizeAnimation from "./SizeAnimation.vue"

import cardMessages from './card.json';

// Merge card specific messages with global messages
const messages = {
    //...configStore.getMessages,
    ...cardMessages,
};


import image from '../assets/images/lastenrad.jpg'; // Replace with your actual image path

</script>

<style scoped>
.card {
    /* Add your card styles here */
}

.header {
    /* Add your header styles here */
}

.text {
    /* Add your text styles here */
}

.image {
    /* Add your image styles here */
    width: 200px;
    max-height:200px;
}

.chart-area {
    /* Add your chart area styles here */
}

.button {
    /* Add your button styles here */
}

.checkbox {
    /* Add your checkbox styles here */
}

.select {
    /* Add your select styles here */
}
</style>


<!-- 
digital-codes: explain where and how to load global messages

GitHub Copilot: To load global messages in a Vue.js application, you typically use a localization library or a global state management solution like Vuex. The code snippet you provided suggests that there is a need to merge card-specific messages with the global messages.

Here are a few steps you can follow to load global messages:

1. Install a localization library or set up a global state management solution like Vuex if you haven't already. Localization libraries such as vue-i18n or vuex-i18n are commonly used in Vue.js applications for managing translations.

2. Create a file to store your global messages. This file can be named something like `messages.js` or `i18n.js`. In this file, you can define an object that contains your global messages in different languages. For example:

   ```javascript
   // messages.js

   export default {
     en: {
       greeting: 'Hello',
       goodbye: 'Goodbye',
       // other global messages
     },
     // other language translations
   };
   ```

3. Import the global messages file in your Vue component where you want to use them. For example, in your `CardTemplate.vue` component, you can import the `messages.js` file like this:

   ```vue
   <script>
   import messages from './messages.js';

   export default {
     // component code
   };
   </script>
   ```

4. Merge the card-specific messages with the global messages. Based on the code snippet you provided, it seems that there is a need to merge the card-specific messages with the global messages. You can use the spread operator (`...`) to achieve this. For example:

   ```vue
   <script>
   import messages from './messages.js';

   export default {
     data() {
       return {
         cardMessages: {
           // card-specific messages
         },
         mergedMessages: {
           ...messages.en, // merge global messages
           ...this.cardMessages, // merge card-specific messages
         },
       };
     },
   };
   </script>
   ```

   In this example, the `mergedMessages` object will contain both the global messages and the card-specific messages. You can then use `mergedMessages` in your component's template to display the appropriate messages.

By following these steps, you can load global messages in your Vue.js application and merge them with card-specific messages as needed. Remember to adjust the code according to your specific localization library or global state management solution.

 
-->