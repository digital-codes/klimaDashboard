<template>
  <div class="card">
    <p>{{ $t($props.name + ".title") }}</p>
    <div class="header">{{ $t($props.name + ".header") }}</div>
    <div class="text">{{ $t($props.name + ".text") }}</div>

    <div class="row">
      <div class="flex flex-col lg6 md12">
        <img :src="basePath + props.logo" alt="Card Image" class="cardimage" />
      </div>
      <div class="flex flex-col lg6 md12">
        <div class="mdcontent" v-html="cardMessages[locale].mdpane"></div>
      </div>
    </div>

   
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
          :false-inner-label='cardMessages[locale].anistop'
          :true-inner-label='cardMessages[locale].anistart'
          class="flex lg2 control switch"/>
    </div>

    <div class="chartpane">
      <!-- Chart component goes here -->
      <SimpleLine :chartDataUri="dataUrl"></SimpleLine>
    </div>

    <div class="chartfooter">
      <!-- source, license, download button -->

      <VaChip outline>
        License: {{ dataLicense }}
      </VaChip>
      <VaChip outline>
        Source: {{ dataUrl }}
      </VaChip>

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

import SimpleLine from "@/components/charts/SimpleLine.vue"

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

// messages i18n
import cardMessages from "./card.json";
const dataUrl = ref(null)
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

watch(dataCtl, (index) => {
  console.log("DataCtl:", index)
})

onBeforeMount(() => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  for (const key in cardMessages) {
    // console.log(`${key}:`, cardMessages[key]);
    if (key === "specs") continue
    messages.value[key][props.name] = cardMessages[key];
    // create new data uris here: use as is if strating with http else prepend base path
    if (dataUrl.value && dataUrl.value.toLowerCase().startsWith("http")) {
      dataUrl.value = cardMessages.specs.data[dataCtl.value].url
    } else {
      dataUrl.value = basePath + cardMessages.specs.data[dataCtl.value].url
    }
    dataLicense.value = cardMessages.specs.data[0].license
  }
  const specs = cardMessages.specs
  if (specs.controls) {
    console.log("Specs:", specs)
    if (specs.controls.range.present) controls.value.range = specs.controls.range
    if (specs.controls.dataswitch.present) controls.value.dataswitch = specs.controls.dataswitch
    if (specs.controls.animate.present) controls.value.animate = specs.controls.animate
    console.log("Ctls:", controls.value)
  }
});

</script>

<style scoped>
/* Add your card styles here */

.control {
  margin-right: 1rem;
  margin-bottom: .3rem;
}

.range {
  min-width: 50%;
}

.switch {
  min-width: 20%;
}

</style>


<style lang="scss" scoped>
@import "vuestic-ui/styles/grid";
</style>
