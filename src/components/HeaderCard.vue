<template>
  <VaCard class="headerCard">
    <div>
      <VaAvatar title="Klima Dashboard" :src="climate" />
      <h1 class="headertitle">{{ $t($props.name + ".title") }}</h1>
      <div class="headerctls">
        <VaButtonGroup grow>
        <VaButton  icon="create" >CO2</VaButton>
        <VaButton  icon="create" >Energie</VaButton>
        <VaButton  icon="add" >Mobilität</VaButton>
        <VaButton  icon="add_circle_outline" >XYZ</VaButton>
      </VaButtonGroup>
      </div>
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
  display: flex;
  flex-wrap: wrap;
  --va-avatar-vertical-align: top;
}

.headertitle {
  margin-left: 1rem;
  display: inline-flex;
}

.headerctls {
  display: inline-flex;
  vertical-align: text-bottom;
  padding-bottom: .2rem;
  margin-left: 1rem
  /* width:50%; */
}

.headertext {
  margin-top: 1rem;
}
</style>
