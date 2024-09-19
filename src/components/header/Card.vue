<template>
  <VaCard class="headerCard">
    <!-- 
    <div>
      <VaAvatar title="Klima Dashboard" :src="modeSwitch == 'dark' ? climate_d : climate_l" :size="breakpoint.smUp ? 'medium' : 'small'" />
      <h1 class="headertitle" :class="breakpoint.xs ? 'headertitlesm' : 'xy'">{{ $t($props.name + ".title") }}</h1>
    </div>

    -->

    <div class="dataheader">
      <VaAvatar title="Klima Dashboard" :src="modeSwitch == 'dark' ? props.icons[1] : props.icons[0]" size="3rem" />
      <h1 class="headertitle" :class="breakpoint.xs ? 'headertitlesm' : ''">{{ $t($props.name + ".title") }}</h1>
    </div>
    <!--
    <FilterInfo :name="infoName" :content="infoContent" :link="infoLink" :img="infoImg" :open="infoOpen" @close="infoOpen=false"/>
    -->


    <!-- 
    <p class="headertext">{{ $t($props.name + ".text") }}</p>
    -->

    <div class="flex xs12">
      <div class="mdcontent" v-html="content[locale]"></div>
    </div>
    <!-- 
    <div class="flex flex-wrap">
      <VaSwitch v-for="(filter, index) in filters" class="filter" :key="index" v-model="filter.value"
        :label="t(props.name + '.' + filter.label)" right-label @input="action(filter.name)" >
        <template #innerLabel>
          <div class="va-text-center">
            <VaIcon :name="filter.icon" />
          </div>
        </template>
          <VaIcon name="info" @click="console.log('click')"/>
        </VaSwitch>
    </div>
  -->
    <div class="flex flex-wrap" style="display:inline-flex;">
      <div v-for="(filter, index) in filters" class="flex flex-wrap">
        <VaButton 
        @click="infoAction(index)" 
        size="small" 
        class="infoicon" 
        aria-label="Help for this Filter" 
        round icon="help" 
        />
        <VaSwitch class="filter" :key="index" v-model="filter.value"
        :label="t(props.name + '.' + filter.label)" right-label @input="action(filter.name)" >
        <template #innerLabel>
          <div class="va-text-center">
            <VaIcon :name="filter.icon" />
          </div>
        </template>
        </VaSwitch>
      </div>
    </div>

    <div class="filterInfo">
        <VaCollapse v-model="infoOpen"
          :header="x"
          class="filterHdr"
        >
          <template #content>
            <hr>
            <h3>{{ infoName }}</h3>
            <img v-if="infoImg" :src="infoImg" alt="infoImg" class="filterImg"/>
            <p v-for="(item,idx) in infoContent.split('\n')" :key="idx">
              {{ infoContent.split('\n')[idx] }}
            </p>
            <a :href="infoLink" target="_blank">{{ infoLink }}</a>
          </template>
        </VaCollapse> 
      </div>
  <!-- 
    infoName.value = t(props.name + "." + filters.value[tag].label)
  infoContent.value = filters.value[tag].content || "No content defined"
  infoLink.value = filters.value[tag].link
  infoImg.value = filters.value[tag].img || null
  infoOpen.value = true
    -->


  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, messages, locale } = useI18n();
import { ref, onBeforeMount, computed, watch, nextTick } from "vue";

import climate_l from "@/assets/icons/dashboard/climate.svg?url"
import climate_d from "@/assets/icons/dashboard/climate_d.svg?url"

import { useBreakpoint } from "vuestic-ui";

import FilterInfo from "@/components/pops/FilterInfo.vue";
const infoName = ref("Infoname")
const infoContent = ref("")
const infoOpen = ref(false)
const infoLink = ref("")
const infoImg = ref(null)

const breakpoint = useBreakpoint();

// mode switch 
import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();
const modeSwitch = ref("light")

watch(() => configStore.getTheme, (newVal, oldVal) => {
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
  icons: {
    type: Array,
    required: true,
    default: [climate_l, climate_d]
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
//import cardContent from "./text.json";

// read localized card messages
//import cardMessages from "./lang.json";

// content pane
const content = ref({});


import { loadMsgs, loadText, loadSpecs } from "@/composables/LoadSpecs"

const infoTag = ref(-1)

const infoAction = async (tag) => {
  console.log("Info action:", tag)
  if (infoOpen.value && (infoTag.value == tag)) {
  //if (infoOpen.value) {
      infoOpen.value = false
    console.log("Close info")
  } else {
    infoTag.value = tag
    infoName.value = t(props.name + "." + filters.value[tag].label)
    infoContent.value = filters.value[tag].content || "No content defined"
    infoLink.value = filters.value[tag].link
    infoImg.value = filters.value[tag].img || null
    infoOpen.value = true
    console.log("Open info")
  }
}

onBeforeMount(async () => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  // localized content
  const supportedLanguages = configStore.getLanguages;

  const cardContent = await loadText(props, supportedLanguages, "hdr")
  const cardMessages = await loadMsgs(props, supportedLanguages, "hdr")
  const cardSpecs = await loadSpecs(props, "hdr")

  // localization data
  for (const key in cardMessages) {
    if (!supportedLanguages.includes(key)) continue;
    messages.value[key][props.name] = cardMessages[key];
  }

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;

    let updatedContent = cardContent[key];
    content.value[key] = updatedContent;
  }

  modeSwitch.value = configStore.getTheme

  // filters, optional
  if (cardSpecs.filters) {
    filters.value = cardSpecs.filters
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

<style scoped lang="scss">

@import '@/style/style.scss';

.infoicon  {
  margin-left: 0;
  margin-right: .5rem;
  --va-background-color: unset  !important;
}

.infoicon :deep(i) {
  color: light-dark($dash-accent-light, $dash-accent-dark)!important;
}

.filterInfo {
  margin-top: 1rem;
  width:100%;
}

.filterInfo :deep(.va-collapse__header) {
  display: none;
}

.filterInfo :deep(.va-collapse__header-wrapper) {
  display: none;
}

.filterInfo :deep(.va-collapse__body-wrapper) {
  overflow-x: hidden;
}

.filterImg {
  width: 30%;
  margin: 1rem 0;
}


</style>
