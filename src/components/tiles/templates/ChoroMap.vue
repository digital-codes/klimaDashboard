<template>
  <div class="card" v-if="confgComplete">
    <div class="dataheader">
      <VaAvatar title="Klima Dashboard" :src="basePath + props.logo" size="3rem" />
      <h1>{{ cardMessages[locale].title }}</h1>
    </div>

    <div class="mdcontent">
      <div v-html="content[locale]"></div>
      <VaCollapse v-if="contentMore[locale] > ''" v-model="showMore" :header="t('more')"
        icon="more_horiz" class="morehdr">
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
        :false-inner-label="cardMessages[locale].dsleft" :true-inner-label="cardMessages[locale].dsright"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />

    </div>

    <div class="chartpane">
      <!-- Chart component goes here -->
      <ChoroMap v-if="chartValid" :dataUrl="dataUrl" :dataName="dataName" :dataIdx="dataCtl ? 1 : 0" 
        :polyUrl="polyUrl" :polyId="polyId" :featureName="featureName" :ariaLabel="ariaLabel" 
      @series="capture">
      </ChoroMap>
    </div>



    <div class="chartfooter">
      <!-- source, license, download button -->

      <VaChip disabled outline>
        {{ $t("license") }}: {{ dataLicense }}
      </VaChip>
      <!-- 
      <VaChip :href="dataUrl" target="_blank" >
        {{ $t($props.name + ".source") }}
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
import { ref, onBeforeMount, onMounted, watch, nextTick } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();


import ChoroMap from "@/components/charts/ChoroPleth.vue";
import { useBreakpoint } from "vuestic-ui";
const breakpoint = useBreakpoint();

const chartInstance = ref(null);

// for relocated base we need to prepend the base path to dynamic imports
const basePath = import.meta.env.BASE_URL;

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
const polyUrl = ref(null);
const polyId = ref(null);
const featureName = ref(null);
const ariaLabel = ref(null)

// needed to force re-render when dataurl reused
const chartValid = ref(true);

// controls
const controls = ref({
  range: false,
  dataswitch: false,
  animate: false,
  type: false,
  stacked: false,
  downloads: { "data": true, "img": true },
});

const rangeCtl = ref(0);
const dataCtl = ref(false);

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

const checkLang = watch(locale, (lang) => {
  // console.log(props.name, " - Locale:", lang, "index:", dataCtl.value ? 1 : 0);
  dataName.value = cardMessages.value[lang].dsname[dataCtl.value ? 1 : 0] || "Data";
  // console.log("dsname:", dataName.value);
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
  polyUrl.value = cardSpecs.value.data[index].polyurl;
  polyId.value = cardSpecs.value.data[index].polyid;
  featureName.value = cardSpecs.value.data[index].feature;
  // name is localized!
  // dataName.value = cardSpecs.value.data[index].name || "Data"
  dataName.value = cardMessages.value[locale.value].dsname[index] || "Data";
  ariaLabel.value = cardMessages.value[locale.value].aria + ": " + dataName.value
  chartValid.value = true;
};

watch(dataCtl, (index) => {
  console.log("DataCtl:", index);
  updateData(index ? 1 : 0);
});


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

const capture = async (data, instance) => {
  console.log("Capture:", data, instance);
  chartInstance.value = instance;
};



onBeforeMount(async () => {
  // Code to execute when the component is mounted
  // localized content
  //currentLocale.value = configStore.getCurrentLocale
  // console.log(props.name, " - Current locale:", locale.value);
  const supportedLanguages = configStore.getLanguages;
  console.log("Props:", props);
  const cardContent = await import(`../${props.section}/${props.part}/${props.name}/text.json`);
  console.log(props.name, " - Card content loaded");

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

  // localization data
  /*
  for (const key in cardMessages) {
    if (!supportedLanguages.includes(key)) continue;
    messages.value[key][props.name] = cardMessages.value[key];
  }
  */

  cardSpecs.value = await import(`../${props.section}/${props.part}/${props.name}/card.json`)
  if (cardSpecs.value.controls) {
    console.log("Specs:", cardSpecs.value);
    if (cardSpecs.value.controls.range.present)
      controls.value.range = cardSpecs.value.controls.range;
    if (cardSpecs.value.controls.dataswitch.present && cardSpecs.value.data.length > 1)
      controls.value.dataswitch = cardSpecs.value.controls.dataswitch;
    if (cardSpecs.value.controls.type.present) controls.value.type = cardSpecs.value.controls.type;
    if (cardSpecs.value.controls.stacked.present)
      controls.value.stacked = cardSpecs.value.controls.stacked;
    if (cardSpecs.value.controls.animate.present)
      controls.value.animate = cardSpecs.value.controls.animate;
    if (cardSpecs.value.controls.downloads !== undefined) {
      controls.value.downloads.img = cardSpecs.value.controls.downloads.image;
      controls.value.downloads.data = cardSpecs.value.controls.downloads.data;
    }
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
  border-color: light-dark($dash-border-light, $dash-border-dark) !important;
  //border:1px solid;
  border-radius: 16px;
}

.slcnt {
  width: 130px;
  text-align: center;
}

.morehdr {
  text-align: left;
}

.smallhdr {
  font-size: 1.5rem;
  line-height: 3rem;
}

</style>

<style lang="scss" scoped>
@import "vuestic-ui/styles/grid";
</style>
