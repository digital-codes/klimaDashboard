<template>
  <VaCard class="footerCard">

    <div class="flex xs12">
      <div class="mdcontent" v-html="content[locale]"></div>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { messages, locale } = useI18n();
import { ref, onBeforeMount } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import { useBreakpoint } from "vuestic-ui";


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

.footerCard {
  margin: .5rem 0 .5rem 0;
  padding: .5rem;
  text-align: left;
  display: flex;
  flex-wrap: wrap;
}


</style>
