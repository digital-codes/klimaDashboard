<template>
  <VaCard class="footerCard">

    <div class="flex xs12">
      <div class="mdcontent" v-html="cardMessages[locale].mdpane"></div>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { messages, locale } = useI18n();
import { onBeforeMount } from "vue";


import { useBreakpoint } from "vuestic-ui";


// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  }
});
console.log("Card name:", props.name);

// messages i18n
import cardMessages from "./card.json";


onBeforeMount(() => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  for (const key in cardMessages) {
    //console.log(`${key}:`, cardMessages[key]);
    messages.value[key][props.name] = cardMessages[key];
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
