<template>
  <VaCard class="headerCard">
    <!-- 
    <div>
      <VaAvatar title="Klima Dashboard" :src="modeSwitch == 'dark' ? climate_d : climate_l" :size="breakpoint.smUp ? 'medium' : 'small'" />
      <h1 class="headertitle" :class="breakpoint.xs ? 'headertitlesm' : 'xy'">{{ $t($props.name + ".title") }}</h1>
    </div>

    -->

    <div class="dataheader">
      <VaAvatar  title="Klima Dashboard" :src="modeSwitch == 'dark' ? climate_d : climate_l" size="3rem"/>
      <h1 class="headertitle" :class="breakpoint.xs ? 'headertitlesm' : 'xy'">{{ $t($props.name + ".title") }}</h1>
    </div>


    
    <!-- 
    <p class="headertext">{{ $t($props.name + ".text") }}</p>
    -->

    <div class="flex xs12">
      <div class="mdcontent" v-html="content[locale]"></div>
    </div>

    <div class="flex flex-wrap">
      <VaSwitch v-for="(filter, index) in filters" class="filter"
      :key="index" 
      v-model="filter.value" 
      :label="t(props.name + '.' + filter.label)" 
      right-label
      @input="action(filter.name)">
        <template #innerLabel>
          <div class="va-text-center">
            <VaIcon :name="filter.icon" />
          </div>
        </template>
      </VaSwitch>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, messages, locale } = useI18n();
import { ref, onBeforeMount, computed, watch } from "vue";

import climate_l from "@/assets/icons/generated/climate_black_on_transparent.svg"
import climate_d from "@/assets/icons/generated/climate_white_on_transparent.svg"

import { useBreakpoint } from "vuestic-ui";

const breakpoint = useBreakpoint();

// mode switch 
import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();
const modeSwitch = ref("light")

watch (() => configStore.getTheme, (newVal, oldVal) => {
  console.log("Mode switch1:", newVal)
  modeSwitch.value = configStore.getTheme
})


/*
const modeSwitch = computed({
  get() {
    return currentPresetName
  }
})
*/

const filters = ref([
  {
    "label": "climate",
    "value": true,
    "icon": "co2",
    "name": "A"
  },
  {
    "label": "energy",
    "value": true,
    "icon": "power",
    "name": "B"
  },
  {
    "label": "mobility",
    "value": true,
    "icon": "directions_bus",
    "name": "C"
  },
  {
    "label": "buildings",
    "value": true,
    "icon": "other_houses",
    "name": "D"
  },
  {
    "label": "other",
    "value": true,
    "icon": "settings",
    "name": "E"
  }
]);

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
  emit("filter", tag);
};

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

  modeSwitch.value = configStore.getTheme

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
  line-height: 3rem;
}

@media screen and (max-width: 639px) {
  .headertitle {
    line-height: 2rem;
  }
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

.filter {
  margin-right: 1rem;
  margin-bottom: .3rem;
}



</style>
