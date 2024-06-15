<template>
  <div class="card">
    <p>{{ $t($props.name + ".title") }}</p>
    <div class="header">{{ $t($props.name + ".header") }}</div>
    <div class="text">{{ $t($props.name + ".text") }}</div>

    <!-- 
    <VaScrollContainer
    class="max-h-52"
    vertical
    >

    <div class="mdcontent" v-html="cardMessages[locale].mdpane"></div>
    
  </VaScrollContainer>
    -->

    <div class="row">
      <div class="flex flex-col lg6 md12">
          <VaImage
            fit="cover"
            class="image"
            :src="props.logo"
          />          
      </div>
      <div class="flex flex-col lg6 md12">
          <div class="mdcontent" v-html="cardMessages[locale].mdpane"></div>
      </div>
    </div>

    <div class="mdcontent" v-html="cardMessages[locale].mdpane"></div>

    <img :src="props.logo" alt="Card Image" class="image" />
    <div class="chart-area">
      <!-- Chart component goes here -->
      <SizeAnimation></SizeAnimation>
    </div>
    <div class="chart-area">
      <!-- Chart component goes here -->
      <ChartTemplate :chartDataUri="cardMessages.specs.dataUrls[0]"></ChartTemplate>
    </div>
    <button class="button">{{ $t($props.name + ".button") }}</button>
    <input type="checkbox" class="checkbox" />
    <select class="select">
      <option value="option1">{{ $t($props.name + ".option1") }}</option>
      <option value="option2">{{ $t($props.name + ".option2") }}</option>
      <option value="option3">{{ $t($props.name + ".option3") }}</option>
    </select>
  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, messages, locale } = useI18n();
import { ref, onBeforeMount } from "vue";

import { computed } from "vue";

import ChartTemplate from "../../charts/ChartTemplate.vue"


// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  },
  logo: {
    type: String,
    default: "/images/tiles/lastenrad.jpg",
    //required: true,
  },
});
console.log("Card name:", props.name);

// messages i18n
import cardMessages from "./card.json";

// chart
import SizeAnimation from "../../charts/SizeAnimation.vue";

onBeforeMount(() => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  for (const key in cardMessages) {
    // console.log(`${key}:`, cardMessages[key]);
    if (key === "specs") continue
    messages.value[key][props.name] = cardMessages[key];
  }
});
</script>

<style scoped>
/* Add your card styles here */
.card {
  /* Add your card styles here */
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.dark {
  /* Add your card styles here */
  color: #fff;
  border: 1px solid #222;
  box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
  background-color: #444;
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
  max-height: 200px;
}

.chart-area {
  /* Add your chart area styles here */
}

.button {
  /* Add your button styles here */
}

scriptbox {
  /* Add your checkbox styles here */
}

.select {
  /* Add your select styles here */
}


</style>


<style lang="scss" scoped>
@import "vuestic-ui/styles/grid";

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
