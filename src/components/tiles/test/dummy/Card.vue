<template>
  <div class="card">
    <p>{{ $t($props.name + ".title") }}</p>
    <div class="header">{{ $t($props.name + ".header") }}</div>
    <div class="text">{{ $t($props.name + ".text") }}</div>

    <div class="row">
      <div class="flex flex-col lg6 md12">
        <img :src="basePath + props.logo" alt="Card Image" class="cardimage" />
      </div>
      <div class="flex flex-col lg6 md12">
          <div class="mdcontent" v-html="cardMessages[locale].mdpane"></div>
      </div>
    </div>
   
    <div class="row">
          <VaSlider v-if="controls.range.present" 
          v-model="rangeCtl" 
          :label="cardMessages[locale].rangetitle"
          class="flex lg6 sm12 xs12 control range"
          track-label-visible
          >
          <template #prepend>
            <VaCounter
              v-model="rangeCtl"
              :min="controls.range.min"
              :max="controls.range.max"
              class="w-[110px]"
              />
            </template>
         </VaSlider>

         <VaSwitch v-if="controls.dataswitch" 
          v-model="dataCtl" 
          :label="cardMessages[locale].dstitle"  
          :false-inner-label='cardMessages[locale].dsleft'
          :true-inner-label='cardMessages[locale].dsright'
          class="flex lg2 control switch"/>

          <VaSwitch v-if="controls.animate" 
           v-model="aniCtl" 
          :label="cardMessages[locale].animation" 
          :false-inner-label='cardMessages[locale].anistop'
          :true-inner-label='cardMessages[locale].anistart'
          class="flex lg2 control switch"/>
    </div>

    <div class="chartpane customchart">
      <!-- Chart component goes here -->
      <SizeAnimation :dataUrl="dataUrl"></SizeAnimation>
    </div>
    <div class="chartpane">
      <!-- Chart component goes here -->
      <ChartTemplate :dataUrl="dataUrl"></ChartTemplate>
    </div>

    <div class="chartfooter">
      <!-- source, license, download button -->

      <VaChip outline>
        License: {{ dataLicense }}
      </VaChip>
      <VaChip outline>
        Source: {{ dataUrl }}
      </VaChip>

      <VaButton round @click="console.log('Click')" icon="download">
        {{ $t($props.name + ".download") }}
      </VaButton>

      <VaButton round @click="console.log('Click')" icon="download">
        {{ $t($props.name + ".downimage") }}
      </VaButton>

    </div>

  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, messages, locale } = useI18n();
import { ref, onBeforeMount, onMounted, watch } from "vue";

import ChartTemplate from "@/components/charts/ChartTemplate.vue"

// for relocated base we need to prepend the base path to dynamic imports
const basePath = import.meta.env.BASE_URL

// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  },
  logo: {
    type: String,
    // no leading / here 
    default: "images/tiles/lastenrad.jpg",
    //required: true,
  },
});
console.log("Card name:", props.name);

// messages i18n
import cardMessages from "./card.json";
const dataUrl = ref(null)
const dataLicense = ref(null)


// chart
import SizeAnimation from "@/components/charts/SizeAnimation.vue";

// controls
const controls = ref({
  range: false,
  dataswitch: false,
  animate: false
})
const rangeCtl = ref(0)
const dataCtl = ref(0)
const aniCtl = ref(0)

watch(dataCtl, (index) => {
  console.log("DataCtl:", index)
  dataUrl.value = cardMessages.specs.data[dataCtl.value?1:0].url
  dataLicense.value = cardMessages.specs.data[dataCtl.value?1:0].license
})

onBeforeMount(() => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  for (const key in cardMessages) {
    // console.log(`${key}:`, cardMessages[key]);
    if (key === "specs") continue
    messages.value[key][props.name] = cardMessages[key];
    // create new data uris here: use as is if strating with http else prepend base path
    if (dataUrl.value && dataUrl.value.toLowerCase().startsWith("http")) {
      dataUrl.value = cardMessages.specs.data[dataCtl.value?1:0].url
    } else {
      dataUrl.value = basePath + cardMessages.specs.data[dataCtl.value?1:0].url
      console.log("data:", dataUrl.value)
    }
    dataLicense.value = cardMessages.specs.data[dataCtl.value?1:0].license
  }
  const specs = cardMessages.specs
  if (specs.controls) {
    console.log("Specs:", specs)
    if (specs.controls.range.present) controls.value.range = specs.controls.range
    if (specs.controls.dataswitch.present) controls.value.dataswitch = specs.controls.dataswitch
    if (specs.controls.animate.present) controls.value.animate = specs.controls.animate
    console.log("Ctls:", controls.value)
  }
});

</script>

<style scoped>
/* Add your card styles here */

.control {
  margin-right: 1rem;
  margin-bottom: .3rem;
}

.range {
  min-width: 50%;
}

.switch {
  min-width: 20%;
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
