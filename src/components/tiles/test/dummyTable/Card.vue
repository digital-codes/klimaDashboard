<template>
  <div class="card">
  <!--

    <p>{{ $t($props.name + ".title") }}</p>
    <div class="header">{{ $t($props.name + ".header") }}</div>
    <div class="text">{{ $t($props.name + ".text") }}</div>
-->

    <div class="dataheader">
      <VaAvatar  title="Klima Dashboard" :src="basePath + props.logo" size="3rem"/>
      <h1 >{{ $t($props.name + ".title") }}</h1>
    </div>

    <div class="mdcontent" v-html="content[locale]"></div>
   
    <div class="row">
          <VaSlider v-if="controls.range.present" 
          v-model="rangeCtl" 
          :label="cardMessages[locale].rangetitle"
          class="flex lg6 sm12 xs12 control range"
          track-label-visible
          >
          <template #prepend>
            <VaCounter
              v-model="rangeCtl"
              :min="controls.range.min"
              :max="controls.range.max"
              class="w-[110px]"
              />
            </template>
         </VaSlider>

         <VaSwitch v-if="controls.dataswitch" 
          v-model="dataCtl" 
          :label="cardMessages[locale].dstitle"  
          :false-inner-label='cardMessages[locale].dsleft'
          :true-inner-label='cardMessages[locale].dsright'
          class="flex lg2 control switch"/>

          <VaSwitch v-if="controls.animate" 
           v-model="aniCtl" 
          :label="cardMessages[locale].animation" 
          :false-inner-label='cardMessages[locale].no'
          :true-inner-label='cardMessages[locale].yes'
          class="flex lg2 control switch"/>
    </div>

    <div class="chartpane">
      <!-- Chart component goes here -->
      <SimpleTable :dataUrl="dataUrl"></SimpleTable>
    </div>

    <div class="chartfooter">
      <!-- source, license, download button -->

      <VaChip disabled outline>
        {{ $t($props.name + ".license") }}: {{ dataLicense }}
      </VaChip>
      <!-- 
      <VaChip :href="dataUrl" target="_blank" >
        {{ $t($props.name + ".source") }}
      </VaChip>
      -->

      <VaButton round @click="console.log('Click')" icon="download">
        {{ $t($props.name + ".download") }}
      </VaButton>

      <VaButton round @click="console.log('Click')" icon="download">
        {{ $t($props.name + ".downimage") }}
      </VaButton>

    </div>

  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, messages, locale } = useI18n();
import { ref, onBeforeMount, onMounted, watch } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import SimpleTable from "@/components/charts/SimpleTable.vue"

// for relocated base we need to prepend the base path to dynamic imports
const basePath = import.meta.env.BASE_URL

// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  },
  logo: {
    type: String,
    // no leading / here 
    default: "images/tiles/lastenrad.jpg",
    //required: true,
  },
});
console.log("Card name:", props.name);

// read localized card content
import cardContent from "./text.json";

// read card specs and localization
import cardMessages from "./card.json";
const dataUrl = ref(null)
const dataName = ref(null)
const dataLicense = ref(null)

// controls
const controls = ref({
  range: false,
  dataswitch: false,
  animate: false
})
const rangeCtl = ref(0)
const dataCtl = ref(0)
const aniCtl = ref(0)

// content pane
const content = ref({})

const checkUrl = (url) => {
    // create new data uris here: use as is if starting with http else prepend base path
    if (url && url.toLowerCase().startsWith("http")) {
    return url
  } else {
    return basePath + url
  }
}

watch(dataCtl, (index) => {
  console.log("DataCtl:", index)
  dataUrl.value = cardMessages.specs.data[dataCtl.value?1:0].url
  dataLicense.value = cardMessages.specs.data[dataCtl.value?1:0].license
})

onBeforeMount(() => {
  // Code to execute when the component is mounted
  // localized content
  const supportedLanguages = configStore.getLanguages;

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;
    content.value[key] = cardContent[key];
  }

  // localization data
  for (const key in cardMessages) {
    if (!supportedLanguages.includes(key)) continue;
    messages.value[key][props.name] = cardMessages[key];
  }

  const specs = cardMessages.specs
// create default data uri here
	dataUrl.value = checkUrl(specs.data[0].url)
	dataLicense.value = specs.data[0].license
	dataName.value = specs.data[0].name

  if (specs.controls) {
    console.log("Specs:", specs)
    if (specs.controls.range.present) controls.value.range = specs.controls.range
    if ((specs.controls.dataswitch.present) && (cardMessages.specs.data.length > 1))controls.value.dataswitch = specs.controls.dataswitch
    if (specs.controls.animate.present) controls.value.animate = specs.controls.animate
    console.log("Ctls:", controls.value)
  }
});

</script>

<style scoped lang="scss">
@use "sass:color";
@use '@/style/colors.scss';
@use "vuestic-ui/styles/grid";

/* Add your card styles here */

.control {
  margin-right: 1rem;
  margin-bottom: .3rem;
}

.range {
  min-width: 50%;
}

.switch {
  min-width: 10%;
  border-color: light-dark(colors.$dash-border-light, colors.$dash-border-dark) !important;
  border:1px solid;
  border-radius: 16px;
}

</style>


