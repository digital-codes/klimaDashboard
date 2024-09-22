<template>
  <VaImage
    :src="logo"
    alt="Dashboard Logo"
    class="hero-image"
    fit="cover"
    >
  </VaImage>

  <VaCard class="homeCard">

    <div class="flex xs12">
      <div class="mdcontent fullheight" v-html="content[locale]"></div>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { messages, locale } = useI18n();
import { ref, onBeforeMount } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

//import logo from "@/assets/logos/logo.png"
import logo from "@/assets/icons/dashboard/climate_color_transparent.svg?url"


// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  }
});
console.log("Card name:", props.name);

// read localized card content
import cardContent from "./text.json";

// read localized card messages
import cardMessages from "./lang.json";

// content pane
const content = ref({});



onBeforeMount(() => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  // localized content
  // localized content
  const supportedLanguages = configStore.getLanguages;

  // localization data
  for (const key in cardMessages) {
    if (!supportedLanguages.includes(key)) continue;
    messages.value[key][props.name] = cardMessages[key];
  }

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;
    content.value[key] = cardContent[key];
  }


});
</script>

<style scoped>
/* Add your card styles here */

.homeCard {
  margin: .5rem 0 .5rem 0;
  padding: .5rem;
  text-align: left;
  display: flex;
  flex-wrap: wrap;
}

.hero-image {
  width: 60%;
  height: auto;
  max-height: 10rem;
  margin-left:20%;
  margin-bottom: 1rem;
  box-shadow: 0 0 5px 5px light-dark(#444,#ccc);
}

</style>
