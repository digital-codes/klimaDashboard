<template>
  <div class="card">
    <div class="dataheader">
      <VaAvatar title="Klima Dashboard" :src="basePath + props.logo" size="3rem" />
      <h1>{{ cardMessages[locale].title }}</h1>
    </div>

    <div class="mdcontent" v-html="content[locale]"></div>

    <p class="weatherdate">{{ $t("measured") }}: {{ weatherDate }}</p>

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

      <VaSwitch v-if="controls.type" v-model="typeCtl" :label="cardMessages[locale].type"
        :false-inner-label="cardMessages[locale].typeleft" :true-inner-label="cardMessages[locale].typeright"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />

      <VaSwitch v-if="controls.stacked" v-model="stackCtl" :label="cardMessages[locale].stacked"
        :false-inner-label="cardMessages[locale].no" :true-inner-label="cardMessages[locale].yes"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />

      <VaSwitch v-if="controls.animate" v-model="aniCtl" :label="cardMessages[locale].animation"
        :false-inner-label="cardMessages[locale].no" :true-inner-label="cardMessages[locale].yes"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />
    </div>

    <div class="row">
      <div class="chartpane flex lg4 sm6 xs12" v-for="i, idx in Object.keys(dataSet)">
        <!-- Chart component goes here -->
        <WeatherGauge v-if="chartValid" :data="dataSet[i]" :dataName="cardMessages[locale][dataColumns[idx]]"
          :dataColumn="dataColumns[idx]" :dataLabels="dataTopics"></WeatherGauge>
      </div>
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

      <VaButton round @click="console.log('Click')" icon="download">
        {{ $t("download") }}
      </VaButton>

      <VaButton round @click="console.log('Click')" icon="download">
        {{ $t("downimage") }}
      </VaButton>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n();
import { ref, onBeforeMount, computed, watch, nextTick } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import WeatherGauge from "@/components/charts/KaWeatherGauge.vue";

// custom data loader
import { loadKaWeatherData } from "./Loader.js"
// data parser for aux data
import Papa from 'papaparse';



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
const dataFormat = ref("json"); // json is default
// we can create series from classes and columns
// NB we cannot do both
// make sure either of the two has to be length 1 (or be empty)
// columns is an array of column names
const dataColumns = ref(null);
// classes is an array starting with the class identifier followed by the class names
const dataClasses = ref(null);
// chart options


const data = ref(null);
const dataSet = ref({});
const dataTopics = ref([]);

// aux data (optional) must be an object with the same structure as the main data
const auxUrl = ref(null);
const auxName = ref(null);
const auxFormat = ref("csv"); // json is default
// result will be merged with data



const meanDate = ref("")
const weatherDate = ref("")

const chartStyle = ref("");


// needed to force re-render when dataurl reused
const chartValid = ref(false);

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

const formatDate = (lang) => {
  if (meanDate.value == "") return ""
  const options = { timeZone: 'Europe/Berlin', day: "numeric", month: "numeric", year: "numeric", hour: 'numeric', minute: 'numeric' }; // Replace 'UTC' with the desired timezone
  const dt = new Date(meanDate.value)
  return dt.toLocaleString(lang, options);
}

const checkLang = watch(locale, (lang) => {
  console.log("Locale:", lang, "index:", dataCtl.value ? 1 : 0);
  dataName.value = cardMessages[lang].dsname[dataCtl.value ? 1 : 0] || "Data";
  console.log("dsname:", dataName.value);
  weatherDate.value = formatDate(lang)
  // updateData(0)
});

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



const updateData = async (index) => {
  const newUrl = checkUrl(cardSpecs.data[index].url);
  //console.log("UpdateData:", index, newUrl)
  if (newUrl === dataUrl.value) {
    chartValid.value = false;
    await nextTick();
  }
  // update refs first
  dataUrl.value = newUrl;
  dataLicense.value = cardSpecs.data[index].license;
  dataFormat.value = cardSpecs.data[index].format || "json";
  dataColumns.value = cardSpecs.data[index].columns || [];
  dataClasses.value = cardSpecs.data[index].classes || [];
  // name is localized!
  // dataName.value = cardSpecs.data[index].name || "Data"
  dataName.value = cardMessages[locale.value].dsname[index] || "Data";
  // then load data
  await loadData()
  await loadAux(cardSpecs)

  chartValid.value = true;
};

// max delay in minutes for data to be considered current
const delayLimit = 100;

// for this tile we use a custom loader. the charts don't load data themselves
const loadData = async () => {
  const url = dataUrl.value
  const columns = dataColumns.value
  const ds = {}
  // get topics from url
  // we recevie data by topic and must rearrange it for the chart by columns
  const urlParms = url.split("?topic=");
  let topics = []
  if ((urlParms.length > 1) && (urlParms[1].length > 0)) {
    for (const t of urlParms[1].split(",")) {
      topics.push(t);
    }
  }
  console.log("Topics:", topics);
  if (topics.length == 0) {
    alert("No topics found in data url");
    return
  }
  dataTopics.value = topics;

  // current time
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone
  //console.log("TZ:", tz)
  const now = new Date()
  //console.log("Now:", now)

  try {
    const dateAndData = await loadKaWeatherData(url);
    data.value = dateAndData.data
    meanDate.value = dateAndData.date
    weatherDate.value = formatDate(locale.value)
    for (const t of topics) {
      const dataPoints = {}
      // get data values from data
      const dt = data.value[t].body[0].data
      for (const d in dt) {
        if (columns.includes(d))
          dataPoints[d] = [dt[d]]
      }
      // get measuring time from measured_at
      dataPoints["measured_at"] = [data.value[t].body[0].measured_at]
      // create time delta from now
      const mt = new Date(data.value[t].body[0].measured_at)
      //console.log("MT:", mt)
      const delta = Math.ceil((now.valueOf() - mt.valueOf()) / (1000 * 60))
      //console.log("Delta (minutes):", delta)
      dataPoints["delta"] = [delta]
      ds[t] = dataPoints;
    }
    // console.log("DataSets1:", ds);

    // second pass: rearrange
    const ds2 = {}
    for (const c of columns) {
      // console.log("Column:", c)
      const dataPoints = {
        mt: [],
        values: []
      }
      for (const t in topics) {
        // console.log("Topic:", t, topics[t])
        // console.log("Data:", ds[topics[t]])
        dataPoints.mt.push(ds[topics[t]].measured_at[0])
        // check delta and insert null if above limit
        dataPoints.values.push(ds[topics[t]].delta[0] < delayLimit ? ds[topics[t]][c][0] : null)
      }
      dataSet.value[c] = dataPoints
    }
    // console.log("DataSets2:", dataSet.value);


  } catch (error) {
    console.error("Error:", error);
  }
}

// for this tile we use a custom loader. the charts don't load data themselves
const loadAux = async (cardSpecs) => {
  if (cardSpecs.data.length < 2) return
  const url = checkUrl(cardSpecs.data[1].url)
  const format = cardSpecs.data[1].format || "csv"
  if (format != "csv") {
    alert("Unsupported format for aux data")
    return
  }

  console.log("Fetching: ", url);
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const auxKeys = [];
  // assume csv
  const csvString = await response.text();
  //console.log("raw CSV:",csvString)
  Papa.parse(csvString, {
    header: true,
    dynamicTyping: true,
    complete: async function (results) {
      //console.log("CSV parsed:", results.data);
      const auxData = results.data.filter((d) => d.measured_at != null);
      // field names must be same as main data!
      //console.log("AuxData:", auxData);
      const auxRow = {
        body: [{
          measured_at: auxData[auxData.length - 1].measured_at,
          data: {
            temperature: auxData[auxData.length - 1].temperature,
            humidity: auxData[auxData.length - 1].humidity,
            pressure: Math.ceil(auxData[auxData.length - 1].pressure * 100),
            irradiation: auxData[auxData.length - 1].irradiation,
          }
        }
        ]
      }
      data.value["lubw"] = auxRow
      dataTopics.value.push("lubw")
      dataSet.value["temperature"].values.push(auxRow.body[0].data.temperature)
      dataSet.value["temperature"].mt.push(auxRow.body[0].measured_at)
      dataSet.value["humidity"].values.push(auxRow.body[0].data.humidity)
      dataSet.value["humidity"].mt.push(auxRow.body[0].measured_at)
      dataSet.value["irradiation"].values.push(auxRow.body[0].data.irradiation)
      dataSet.value["irradiation"].mt.push(auxRow.body[0].measured_at)
      dataSet.value["pressure"].values.push(auxRow.body[0].data.pressure)
      dataSet.value["pressure"].mt.push(auxRow.body[0].measured_at)
    },
  });
}


onBeforeMount(async () => {
  // Code to execute when the component is mounted
  // localized content
  const supportedLanguages = configStore.getLanguages;

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;
    content.value[key] = cardContent[key];
  }

  const specs = cardSpecs;
  if (specs.controls) {
    if (specs.controls.range.present)
      controls.value.range = specs.controls.range;
    if (specs.controls.dataswitch.present && cardSpecs.data.length > 1)
      controls.value.dataswitch = specs.controls.dataswitch;
    if (specs.controls.type.present) controls.value.type = specs.controls.type;
    if (specs.controls.stacked.present)
      controls.value.stacked = specs.controls.stacked;
    if (specs.controls.animate.present)
      controls.value.animate = specs.controls.animate;
  }
  updateData(0);
});
</script>

<style scoped lang="scss">
@use "sass:color";
@use '@/style/colors.scss';
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

