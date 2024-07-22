<template>
  <div class="card" v-if="confgComplete">
    <div class="dataheader">
      <VaAvatar title="Klima Dashboard" :src="basePath + props.logo" size="3rem" />
      <h1>{{ cardMessages[locale].title }}</h1>
    </div>

    <div class="mdcontent" v-html="content[locale]"></div>

    <div class="row">
      <VaSlider v-if="controls.range.present" v-model="rangeCtl" :label="cardMessages[locale].rangetitle"
        :min="controls.range.min" :max="controls.range.max" :step="controls.range.step" :disabled="stackCtl && (rangeAxis === 'y')"
        class="flex lg6 sm12 xs12 control range" track-label-visible>
        <template #prepend>
          <VaCounter v-model="rangeCtl" :min="controls.range.min" :max="controls.range.max" class="slcnt" />
        </template>
      </VaSlider>

      <VaSwitch v-if="controls.dataswitch" v-model="dataCtl" :label="cardMessages[locale].dstitle"
        :false-inner-label="cardMessages[locale].dsleft" :true-inner-label="cardMessages[locale].dsright"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />

      <VaSwitch v-if="controls.type" v-model="typeCtl" :label="cardMessages[locale].type"
        :false-inner-label="cardMessages[locale].typeleft" :true-inner-label="cardMessages[locale].typeright"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />

      <VaSwitch v-if="controls.stacked" v-model="stackCtl" :label="cardMessages[locale].stacked"
        :false-inner-label="cardMessages[locale].no" :true-inner-label="cardMessages[locale].yes"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />

      <VaSwitch v-if="controls.animate" ref="animateSwitch" v-model="aniCtl" :label="cardMessages[locale].animation"
        :false-inner-label="cardMessages[locale].no" :true-inner-label="cardMessages[locale].yes"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />
    </div>

    <div class="chartpane">
      <!-- Chart component goes here -->
      <SimpleLine v-if="chartValid" :dataUrl="dataUrl" :dataName="dataName" :dataIdx="dataCtl ? 1 : 0"
        :dataColumns="dataColumns" :dataClasses="dataClasses" :dataX="dataX" :dataY="dataY" :rangeValue="rangeCtl"
        :rangeAxis="rangeAxis" :dataFormat="dataFormat" :labelX="labelX" :labelY="labelY" :type="chartType"
        :stacked="stackCtl" :animate="aniCtl" :ariaLabel="ariaLabel" :locale="chartLocale" @xrange="setXrange"
        @yrange="setYrange"></SimpleLine>
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
        {{ cardMessages[locale].download }}
      </VaButton>

      <VaButton round @click="console.log('Click')" icon="download">
        {{ cardMessages[locale].downimage }}
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

// config flaag
const confgComplete = ref(false);
// read localized card content
//import cardContent from "./text.json";

// read localized card messages
// import cardMessages from "./lang.json";
const cardMessages = ref({});

// read card cardSpecs.value
//import cardSpecs from "./card.json";
const cardSpecs = ref({});

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
const rangeAxis = ref("");
const dataCtl = ref(false);
const aniCtl = ref(false);
const typeCtl = ref(false);
const stackCtl = ref(false);
const chartType = ref("line");
const chartLocale = ref(locale);
const ariaLabel = ref("Aria LineChart");

const animateSwitch = ref(null);

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
  // console.log(props.name," - Locale:", lang, "index:", dataCtl.value ? 1 : 0);
  dataName.value = cardMessages.value[lang].dsname[dataCtl.value ? 1 : 0] || "Data";
  // console.log("dsname:", dataName.value);
  ariaLabel.value = cardMessages.value[lang].aria + ": " + dataName.value
  chartLocale.value = lang;
  // updateData(0)
});

const updateData = async (index) => {
  const newUrl = checkUrl(cardSpecs.value.data[index].url);
  //console.log("UpdateData:", index, newUrl)
  if (newUrl === dataUrl.value) {
    chartValid.value = false;
    await nextTick();
  }
  dataUrl.value = newUrl;
  dataLicense.value = cardSpecs.value.data[index].license;
  dataX.value = cardSpecs.value.data[index].xaxis || "";
  dataY.value = cardSpecs.value.data[index].yaxis || "";
  labelX.value = cardSpecs.value.data[index].xlabel || "";
  labelY.value = cardSpecs.value.data[index].ylabel || "";
  dataFormat.value = cardSpecs.value.data[index].format || "json";
  dataColumns.value = cardSpecs.value.data[index].columns || [];
  dataClasses.value = cardSpecs.value.data[index].classes || [];
  // name is localized!
  // dataName.value = cardSpecs.value.data[index].name || "Data"
  dataName.value = cardMessages.value[locale.value].dsname[index] || "Data";
  ariaLabel.value = cardMessages.value[locale.value].aria + ": " + dataName.value
  chartValid.value = true;
};


watch(stackCtl, () => {
  // also reset animation when stacking changed
  aniCtl.value = false;
});



watch(dataCtl, (index) => {
  console.log("DataCtl:", index);
  updateData(index ? 1 : 0);
  // also reset animation
  aniCtl.value = false;
});

watch(typeCtl, (index) => {
  console.log("TypeCtl:", index);
  chartType.value = index
    ? controls.value.type.options[1]
    : controls.value.type.options[0];
});


const setXrange = async (range) => {
  console.log("Xrange:", range);
  if (rangeAxis.value === "x") {
    rangeCtl.value = 0 // force update 
    await nextTick()
    controls.value.range.min = range[0]
    controls.value.range.max = range[1]
    rangeCtl.value = controls.value.range.min;
    controls.value.range.step = 1 // use 1 for x axis steps
  }
};

const setYrange = async (range) => {
  console.log("Yrange:", range);
  if (rangeAxis.value === "y") {
    /*
    rangeCtl.value = 0 // force update. probably not needed for y
    await nextTick()
    */
    controls.value.range.min = range[0]
    controls.value.range.max = range[1]
    rangeCtl.value = controls.value.range.max;
    controls.value.range.step = Math.ceil(controls.value.range.max / 10)
  }
};



onBeforeMount(async () => {
  // Code to execute when the component is mounted
  // localized content
  //currentLocale.value = configStore.getCurrentLocale
  console.log(props.name, " - Current locale:", locale.value);
  const supportedLanguages = configStore.getLanguages;

  const cardContent = await import(`../${props.name}/text.json`);
  console.log(props.name, " - Card content loaded");

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;
    content.value[key] = cardContent[key];
  }

  cardMessages.value = await import(`../${props.name}/lang.json`)
  console.log(props.name, " - Card messages loaded");

  for (const key in supportedLanguages) {
    const lang = supportedLanguages[key]
    console.log(key, cardMessages.value[lang])
    if (cardMessages.value[lang].aria === undefined)
      cardMessages.value[lang].aria = "Aria " + lang;
  }

  // localization data
  /*
  for (const key in cardMessages) {
    if (!supportedLanguages.includes(key)) continue;
    messages.value[key][props.name] = cardMessages.value[key];
  }
  */

  cardSpecs.value = await import(`../${props.name}/card.json`)
  console.log(props.name, " - Card cardSpecs.value loaded");
  if (cardSpecs.value.controls) {
    console.log("Specs:", cardSpecs.value);
    if (cardSpecs.value.controls.range.present) {
      controls.value.range = cardSpecs.value.controls.range;
      console.log("Range:", controls.value.range);
      /*
      if (controls.value.range.step === undefined) {
        controls.value.range.step = Math.ceil(controls.value.range.max / 10)
      }
      rangeCtl.value = cardSpecs.value.controls.range.max;
      */
      rangeAxis.value = cardSpecs.value.controls.range.axis || "y";
    }
    else {
      controls.value.range = false;
    }
    if (cardSpecs.value.controls.dataswitch.present && cardSpecs.value.data.length > 1)
      controls.value.dataswitch = cardSpecs.value.controls.dataswitch;
    else controls.value.dataswitch = false;
    if (cardSpecs.value.controls.type) {
      chartType.value = cardSpecs.value.controls.type.options[0];
      console.log("Type:", chartType.value);
      if (cardSpecs.value.controls.type.present) controls.value.type = cardSpecs.value.controls.type;
    } else {
      controls.value.type = false;
    }

    if (cardSpecs.value.controls.stacked.present)
      controls.value.stacked = cardSpecs.value.controls.stacked;
    else controls.value.stacked = false;
    if (cardSpecs.value.controls.animate.present)
      controls.value.animate = cardSpecs.value.controls.animate;
    else controls.value.animate = false;
    console.log("Ctls:", controls.value);
  }
  confgComplete.value = true
  updateData(0);
});
</script>

<style scoped lang="scss">
@import "@/style/colors.scss";

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
  border-color: light-dark($light-blue, $dark-orange) !important;
  //border:1px solid;
  border-radius: 16px;
}

.slcnt {
  width: 130px;
  text-align: center;
}

</style>

<style lang="scss" scoped>
@import "vuestic-ui/styles/grid";
</style>
