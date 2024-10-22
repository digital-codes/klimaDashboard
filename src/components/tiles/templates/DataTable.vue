<template>
  <div class="card" v-if="configComplete">
    <div class="dataheader">
      <VaAvatar title="Klima Dashboard" :src="basePath + props.logo" size="3rem" />
      <h1>{{ cardMessages[locale].title }}</h1>

      <div v-if="breakpoint.xs">

        <div style="display:flex;margin-left: 1rem;" v-if="progress > 0">
          <VaIcon class="material-icons-outlined" :name="progressIcon" :color="progressColor" style="line-height:3rem;"
            size="1.5rem" />
        </div>
      </div>
      <div v-else>
        <div style="display:flex;margin-left: 1rem;" v-if="progress > 0">
          <span style="font-size:1.5rem;line-height:3rem;margin-right:.5rem;">{{ $t("progress") }}:</span>
          <VaIcon class="material-icons-outlined" :name="progressIcon" :color="progressColor" style="line-height:3rem;"
            size="1.5rem" />
          <span style="font-size:1rem;line-height:3rem;margin-left:.2rem;">{{ progressText }}</span>
        </div>
      </div>

      <!-- 
      <div style="display:flex;margin-left: 1rem;" v-if="progress > 0">
        <span style="font-size:1.5rem;line-height:3rem;margin-right:.5rem;">{{ $t("progress") }}:</span>
        <VaIcon class="material-icons-outlined" :name="progressIcon" :color="progressColor" style="line-height:3rem;"
          size="1.5rem" />
        <span style="font-size:1rem;line-height:3rem;margin-left:.2rem;">{{ progressText }}</span>
      </div>
      -->

    </div>

    <div class="mdcontent">
      <div v-html="content[locale]"></div>
      <VaCollapse v-if="contentMore[locale] > ''" v-model="showMore" :header="t('more')" icon="more_horiz"
        class="morehdr">
        <template #content>
          <div v-html="contentMore[locale]"></div>
        </template>
      </VaCollapse>

    </div>


    <div class="row">
      <VaSlider v-if="controls.range.present" v-model="rangeCtl" :label="cardMessages[locale].rangetitle"
        class="flex lg6 sm12 xs12 control range" track-label-visible>
        <template #prepend>
          <VaCounter v-model="rangeCtl" :min="controls.range.min" :max="controls.range.max" class="w-[110px]" />
        </template>
      </VaSlider>

      <VaSwitch v-if="controls.dataswitch" v-model="dataCtl" :label="cardMessages[locale].dstitle"
        :false-inner-label="t('dsleft')" :true-inner-label="t('dsright')"
        class="flex lg2 control switch" />

      <VaSwitch v-if="controls.animate" v-model="aniCtl" :label="cardMessages[locale].animation"
        :false-inner-label="t('no')" :true-inner-label="t('yes')"
        class="flex lg2 control switch" />
    </div>

    <div class="chartpane">
      <!-- Chart component goes here -->
      <SimpleTable v-if="chartValid" :dataUrl="dataUrl" :dataIdx="dataCtl ? 1 : 0"
        :dataColumns="dataColumns" :dataClasses="dataClasses" 
         :dataFormat="dataFormat" :dataDelimiter="dataDelimiter" 
         :ariaLabel="ariaLabel" 
        @series="capture"></SimpleTable>
    </div>

    <div class="chartfooter">
      <!-- source, license, download button -->

      <VaChip disabled outline>
        {{ $t("license")  }}: {{ dataLicense }}
      </VaChip>
      <!-- 
      <VaChip :href="dataUrl" target="_blank" >
        {{ $t("source") }}
      </VaChip>
      -->

      <VaButton round @click="csvDown" icon="download" v-if="controls.downloads.data">
        {{ $t("download") }}
      </VaButton>

      <VaButton round @click="imgDown" icon="download" v-if="controls.downloads.img">
        {{ $t("downimage") }}
      </VaButton>

    </div>

  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n();
import { ref, onBeforeMount, onMounted, watch, nextTick, computed } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import { useBreakpoint } from "vuestic-ui";
const breakpoint = useBreakpoint();

import { downloadDataAsCSV, downloadDataAsJSON } from "@/composables/DataDown";

// for relocated base we need to prepend the base path to dynamic imports
const basePath = import.meta.env.BASE_URL;

import SimpleTable from "@/components/charts/SimpleTable.vue";



// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  },
  section: {
    type: String,
    default: "",
  },
  part: {
    type: String,
    default: "",
  },
  logo: {
    type: String,
    // no leading / here
    default: "images/tiles/lastenrad.jpg",
    //required: true,
  },
});
console.log("Card name:", props.name);

// config flag
const configComplete = ref(false);
// read localized card content
//import cardContent from "./text.json";

// read localized card messages
// import cardMessages from "./lang.json";
const cardMessages = ref({});

// read card cardSpecs.value
//import cardSpecs from "./card.json";
const cardSpecs = ref({});
const progress = ref(0);

const progressText = computed(() => {
  switch (progress.value) {
    case 1:
      return t("unknown")
    case 2:
      return t("delayed")
    case 3:
    case 4:
      return t("inprogress")
    default:
      return t("completed")
  }
});

const progressIcon = computed(() => {
  switch (progress.value) {
    case 1:
      return "help_outline";
    case 2:
      return "alarm_on"
    case 3:
    case 4:
      return "schedule";
    default:
      return "check_circle_outline";
  }
});

const progressColor = computed(() => {
  switch (progress.value) {
    case 1:
      return "#808080";
    case 2:
      return "#ff0000"
    case 3:
    case 4:
      return "#0000ff";
    default:
      return "#00ff00";
  }
});

const dataUrl = ref(null);
const dataName = ref(null);
const dataLicense = ref(null);
const dataFormat = ref("json"); // json is default
const dataDelimiter = ref(";"); // csv default ; and US numbers
// we can create series from classes and columns
// NB we cannot do both
// make sure either of the two has to be length 1 (or be empty)
// columns is an array of column names
const dataColumns = ref(null);
// classes is an array starting with the class identifier followed by the class names
const dataClasses = ref(null);

// needed to force re-render when dataurl reused
const chartValid = ref(true);

// controls
const controls = ref({
  range: false,
  dataswitch: false,
  downloads: { "data": true, "img": true },
});

const dataCtl = ref(false);
const chartLocale = ref(locale);
const ariaLabel = ref("Aria LineChart");

const downCtl = ref({ "data": true, "img": true })

// data from chart => download
const seriesData = ref(null);


// content pane
const content = ref({});
const contentMore = ref({});
const showMore = ref(false);

const checkUrl = (url) => {
  // create new data uris here: use as is if starting with http else prepend base path
  if (url && url.toLowerCase().startsWith("http")) {
    return url;
  } else {
    return basePath + url;
  }
};

watch(locale, (lang) => {
  console.log(props.name, " - Locale:", lang, "index:", dataCtl.value ? 1 : 0);
  dataName.value = cardMessages.value[lang].dsname[dataCtl.value ? 1 : 0] || "Data";
  // console.log("dsname:", dataName.value);
  ariaLabel.value = cardMessages.value[lang].aria + ": " + dataName.value
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
  dataFormat.value = cardSpecs.value.data[index].format || "json";
  dataDelimiter.value = cardSpecs.value.data[index].delimiter || ";";
  dataColumns.value = cardSpecs.value.data[index].columns || [];
  dataClasses.value = cardSpecs.value.data[index].classes || [];
  // name is localized!
  // dataName.value = cardSpecs.value.data[index].name || "Data"
  dataName.value = cardMessages.value[locale.value].dsname[index] || "Data";
  ariaLabel.value = cardMessages.value[locale.value].aria + ": " + dataName.value
  chartValid.value = true;
};


const csvDown = () => {
  if (!seriesData.value) return;
  const url = downloadDataAsCSV(seriesData.value)
  if (!url) return;
  const filename = dataName.value + ".csv";
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const imgDown = () => {
  if (!chartInstance.value) return;
  const imgUrl = chartInstance.value.getDataURL({
    pixelRatio: 2,
    backgroundColor: '#fff'
  });
  const filename = dataName.value + ".png";
  const link = document.createElement("a");
  link.href = imgUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};


watch(dataCtl, (index) => {
  console.log("DataCtl:", index);
  updateData(index ? 1 : 0);
});

const capture = async (data, instance) => {
  chartInstance.value = instance;
  // capture data from chart after update
  seriesData.value = data;
};



onBeforeMount(async () => {
  // Code to execute when the component is mounted
  // localized content
  //currentLocale.value = configStore.getCurrentLocale
  // a <hr> in the text splits the content into two parts: main content and more content
  const supportedLanguages = configStore.getLanguages;
  console.log("Props:", props);
  const cardContent = await import(`../${props.section}/${props.part}/${props.name}/text.json`);
  //const cardContent = await import(`../tileSpecs/${props.name}/text.json`); 

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;
    const txt = cardContent[key].split("<hr>");
    content.value[key] = txt[0] || "";
    contentMore.value[key] = txt[1] || "";
  }

  cardMessages.value = await import(`../${props.section}/${props.part}/${props.name}/lang.json`)

  for (const key in supportedLanguages) {
    const lang = supportedLanguages[key]
    if (cardMessages.value[lang].aria === undefined)
      cardMessages.value[lang].aria = "Aria " + lang;
  }


  cardSpecs.value = await import(`../${props.section}/${props.part}/${props.name}/card.json`)
  if (cardSpecs.value.controls) {
    if (cardSpecs.value.controls.dataswitch.present && cardSpecs.value.data.length > 1)
      controls.value.dataswitch = cardSpecs.value.controls.dataswitch;
    else controls.value.dataswitch = false;
    if (cardSpecs.value.controls.downloads.present) {
      controls.value.downloads = cardSpecs.value.controls.downloads;
    }
    else controls.value.dataswitch = false;
  }
  console.log("CardSpecs:", cardSpecs.value);
  configComplete.value = true
  updateData(0);
});
</script>

<style scoped lang="scss">
@use "@/style/colors.scss";
@use "vuestic-ui/styles/grid";

/* Add your card styles here */

.control {
  margin-right: 1rem;
  margin-bottom: 0.3rem;
}

.range {
  min-width: 50%;
}

.rangeCnt {
  text-align: left;
}

.rangeCnt :deep(.va-slider__input-wrapper) {
  //display:none;
  flex: unset;
}

.rangeCnt :deep(.va-slider__container) {
  display: none;
}

.switch {
  min-width: 10%;
  border-color: light-dark(colors.$dash-border-light, colors.$dash-border-dark) !important;
  //border:1px solid;
  border-radius: 16px;
}

.morehdr {
  text-align: left;
}

.smallhdr {
  font-size: 1.5rem;
  line-height: 3rem;
}
</style>

