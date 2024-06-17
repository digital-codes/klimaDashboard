<template>
  <VaCard class="headerCard">
  <div>
    <VaAvatar title="Klima Dashboard" :src="climate" />
    <h1 class="headertitle">{{ $t($props.name + ".title") }}</h1>
    </div>
    <p class="headertext">{{ $t($props.name + ".text") }}</p>
  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, messages, locale } = useI18n();
import { ref, onBeforeMount } from "vue";

import climate from "/icons/climate.svg";

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
import cardMessages from "./headerCard.json";


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

.headerCard {
  margin: .5rem 0 .5rem 0;
  padding: .5rem;
  text-align: left;
  --va-avatar-vertical-align: top;
}

.headertitle {
  margin-left: 1rem;
  display:inline-block;
}

.headertext {
  margin-top: 1rem;
}

</style>
