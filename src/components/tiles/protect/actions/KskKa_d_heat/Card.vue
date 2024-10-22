<template>
  <div class="card">
    <div class="dataheader">
      <VaAvatar
        title="Klima Dashboard"
        :src="basePath + props.logo"
        size="3rem"
      />
      <h1>{{ $t($props.name + ".title") }}</h1>
    </div>

    <div class="mdcontent" v-html="content[locale]"></div>

    <div class="row">
      <VaSlider
        v-if="controls.range.present"
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

      <VaSwitch
        v-if="controls.dataswitch"
        v-model="dataCtl"
        :label="cardMessages[locale].dstitle"
        :false-inner-label="cardMessages[locale].dsleft"
        :true-inner-label="cardMessages[locale].dsright"
        class="flex lg2 control switch"
        offColor="rgba(100,100,100,.4)"
        leftLabel
      />

      <VaSwitch
        v-if="controls.type"
        v-model="typeCtl"
        :label="cardMessages[locale].type"
        :false-inner-label="cardMessages[locale].typeleft"
        :true-inner-label="cardMessages[locale].typeright"
        class="flex lg2 control switch"
        offColor="rgba(100,100,100,.4)"
        leftLabel
      />

      <VaSwitch
        v-if="controls.stacked"
        v-model="stackCtl"
        :label="cardMessages[locale].stacked"
        :false-inner-label="cardMessages[locale].no"
        :true-inner-label="cardMessages[locale].yes"
        class="flex lg2 control switch"
        offColor="rgba(100,100,100,.4)"
        leftLabel
      />

      <VaSwitch
        v-if="controls.animate"
        v-model="aniCtl"
        :label="cardMessages[locale].animation"
        :false-inner-label="cardMessages[locale].no"
        :true-inner-label="cardMessages[locale].yes"
        class="flex lg2 control switch"
        offColor="rgba(100,100,100,.4)"
        leftLabel
      />
    </div>

    <div class="chartpane">
      <!-- Chart component goes here -->
      <SimpleLine
        v-if="chartValid"
        :dataUrl="dataUrl"
        :dataName="dataName"
        :dataIdx="dataCtl ? 1 : 0"
        :dataColumns="dataColumns"
        :dataClasses="dataClasses"
        :dataX="dataX"
        :dataY="dataY"
        :dataFormat="dataFormat"
        :labelX="labelX"
        :labelY="labelY"
        :type="chartType"
        :stacked="stackCtl"
        :animate="aniCtl"
      ></SimpleLine>
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
import { ref, onBeforeMount, onMounted, watch, nextTick } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();


import SimpleLine from "@/components/charts/SimpleLine.vue";

// for relocated base we need to prepend the base path to dynamic imports
const basePath = import.meta.env.BASE_URL;

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

// read localized card messages
import cardMessages from "./lang.json";

// read card specs
import cardSpecs from "./card.json";
const dataUrl = ref(null);
const dataName = ref(null);
const dataLicense = ref(null);
const dataX = ref(null);
const dataY = ref(null);
const labelX = ref(null);
const labelY = ref(null);
const dataFormat = ref("json"); // json is default
// we can create series from classes and columns
// NB we cannot do both
// make sure either of the two has to be length 1 (or be empty)
// columns is an array of column names
const dataColumns = ref(null);
// classes is an array starting with the class identifier followed by the class names
const dataClasses = ref(null);
// chart options
const dataType = ref(null);
const dataStacked = ref(false);

// needed to force re-render when dataurl reused
const chartValid = ref(true);

// controls
const controls = ref({
  range: false,
  dataswitch: false,
  animate: false,
  type: false,
  stacked: false,
});

const rangeCtl = ref(0);
const dataCtl = ref(false);
const aniCtl = ref(false);
const typeCtl = ref(false);
const stackCtl = ref(false);
const chartType = ref("line");

// content pane
const content = ref({});

const checkUrl = (url) => {
  // create new data uris here: use as is if starting with http else prepend base path
  if (url && url.toLowerCase().startsWith("http")) {
    return url;
  } else {
    return basePath + url;
  }
};

const checkLang = watch(locale, (lang) => {
  console.log("Locale:", lang, "index:", dataCtl.value ? 1 : 0);
  dataName.value = cardMessages[lang].dsname[dataCtl.value ? 1 : 0] || "Data";
  console.log("dsname:", dataName.value);
  // updateData(0)
});

const updateData = async (index) => {
  const newUrl = checkUrl(cardSpecs.data[index].url);
  //console.log("UpdateData:", index, newUrl)
  if (newUrl === dataUrl.value) {
    chartValid.value = false;
    await nextTick();
  }
  dataUrl.value = newUrl;
  dataLicense.value = cardSpecs.data[index].license;
  dataX.value = cardSpecs.data[index].xaxis || "";
  dataY.value = cardSpecs.data[index].yaxis || "";
  labelX.value = cardSpecs.data[index].xlabel || "";
  labelY.value = cardSpecs.data[index].ylabel || "";
  dataFormat.value = cardSpecs.data[index].format || "json";
  dataColumns.value = cardSpecs.data[index].columns || [];
  dataClasses.value = cardSpecs.data[index].classes || [];
  // name is localized!
  // dataName.value = cardSpecs.data[index].name || "Data"
  dataName.value = cardMessages[locale.value].dsname[index] || "Data";
  chartValid.value = true;
};

watch(dataCtl, (index) => {
  console.log("DataCtl:", index);
  updateData(index ? 1 : 0);
});

watch(typeCtl, (index) => {
  console.log("TypeCtl:", index);
  chartType.value = index
    ? controls.value.type.options[1]
    : controls.value.type.options[0];
});

onBeforeMount(async () => {
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

  const specs = cardSpecs;
  if (specs.controls) {
    console.log("Specs:", specs);
    if (specs.controls.range.present)
      controls.value.range = specs.controls.range;
    if (specs.controls.dataswitch.present && cardSpecs.data.length > 1)
      controls.value.dataswitch = specs.controls.dataswitch;
    if (specs.controls.type.present) controls.value.type = specs.controls.type;
    if (specs.controls.stacked.present)
      controls.value.stacked = specs.controls.stacked;
    if (specs.controls.animate.present)
      controls.value.animate = specs.controls.animate;
    console.log("Ctls:", controls.value);
  }
  updateData(0);
});
</script>

<style scoped lang="scss">
@ûse "@/style/colors.scss";
@use "vuestic-ui/styles/grid";

/* Add your card styles here */

.control {
  margin-right: 1rem;
  margin-bottom: 0.3rem;
}

.range {
  min-width: 50%;
}

.switch {
  min-width: 10%;
  border-color: light-dark(colors.$dash-border-light, colors.$dash-border-dark) !important;
  //border:1px solid;
  border-radius: 16px;
}
</style>

