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
      <div class="mdcontent fullheight" v-html="cardMessages[locale].mdpane"></div>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { messages, locale } = useI18n();
import { onBeforeMount } from "vue";

import logo from "@/assets/logos/logo.png"


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
