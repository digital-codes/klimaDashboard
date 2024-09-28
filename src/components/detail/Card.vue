<template>
  <VaCard class="detailCard">

    <h2> {{  props.topic  }}</h2>
    <div class="flex xs12">
      <div class="mdcontent fullheight" v-html="cardMessages[locale].mdpane"></div>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { messages, locale } = useI18n();
import { onBeforeMount } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import { useBreakpoint } from "vuestic-ui";


// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  },
  topic: {
    type: String,
    required: true
  }
});

console.log("Card name:", props.name);

// messages i18n
import cardMessages from "./card.json";


onBeforeMount(() => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  const supportedLanguages = configStore.getLanguages;

  // localization data
  for (const key in cardMessages) {
    if (!supportedLanguages.includes(key)) continue;
    messages.value[key][props.name] = cardMessages[key];
  }
});
</script>

<style scoped>
/* Add your card styles here */

.detailCard {
  margin: .5rem 0 .5rem 0;
  padding: .5rem;
  text-align: left;
  display: flex;
  flex-wrap: wrap;
}


</style>
