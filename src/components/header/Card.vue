<template>
  <VaCard class="headerCard">
    <div>
      <VaAvatar title="Klima Dashboard" :src="climate" :size="breakpoint.smUp ? 'medium' : 'small'" />
      <h1 class="headertitle" :class="breakpoint.xs ? 'headertitlesm' : 'xy'">{{ $t($props.name + ".title") }}</h1>
    </div>
    <!-- 
    <p class="headertext">{{ $t($props.name + ".text") }}</p>
    -->

    <div class="flex xs12">
      <div class="mdcontent" v-html="cardMessages[locale].mdpane"></div>
    </div>

    <div v-if="breakpoint.mdUp" class="flex xs12 headerctls">
      <VaButtonGroup grow >
        <VaButton icon="create" @click="action('A')" class="filterbtn" >CO2</VaButton>
        <VaButton icon="create" @click="action('B')" class="filterbtn">Energie</VaButton>
        <VaButton icon="add" @click="action('C')">Mobilität</VaButton>
        <VaButton icon="add_circle_outline" @click="action('D')">XYZ</VaButton>
        <VaButton icon="add" @click="action('E')">Mobilität</VaButton>
      </VaButtonGroup>
    </div>
    <div v-else class="flex xs12 headerctlssm">
      <VaButtonGroup grow>
        <VaButton icon="create" @click="action('A')" class="filterbtn">CO2</VaButton>
        <VaButton icon="create" @click="action('B')" class="filterbtn">Energie</VaButton>
      </VaButtonGroup>
      <VaButtonGroup grow>
        <VaButton icon="add" @click="action('C')">Mobilität</VaButton>
        <VaButton icon="add_circle_outline" @click="action('D')">XYZ</VaButton>
      </VaButtonGroup>
      <VaButtonGroup grow>
        <VaButton icon="add" @click="action('E')">Mobilität</VaButton>
      </VaButtonGroup>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, messages, locale } = useI18n();
import { ref, onBeforeMount } from "vue";

import climate from "/icons/climate.svg";

import { useBreakpoint } from "vuestic-ui";

const breakpoint = useBreakpoint();

/*
const brkPnt = () => {
  if (breakpoint.xs) {
    console.log("It's XS breakpoint!");
  } else {
    console.log("Not XS")
  }
};
*/

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

const emit = defineEmits(["filter"]);
const action = (tag) => {
  emit("filter",tag);
};

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

.headertitlesm {
  margin-left: .5rem;
  font-size: 2rem;
}

.headerctls {
  display: inline-flex;
  vertical-align: text-bottom;
  padding-bottom: .2rem;
  margin-left: 1rem;
  --va-button-group-button-margin: .1rem;
}

.headerctlssm {
  display: flex;
  flex-wrap: wrap;
  padding-bottom: .2rem;
  --va-button-group-button-margin: .1rem;
}

.headertext {
  margin-top: 1rem;
}

.filterbtn {
  border: solid 3px #f00 !important;
}

</style>


