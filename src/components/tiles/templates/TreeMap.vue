<template>
  <div class="card" v-if="confgComplete">
    <div class="dataheader">
      <VaAvatar  title="Klima Dashboard" :src="basePath + props.logo" size="3rem"/>
      <h1>{{ cardMessages[locale].title }}</h1>
    </div>


    <div class="mdcontent">
      <div v-html="content[locale]"></div>
      <VaCollapse v-if="contentMore[locale] > ''" v-model="showMore" :header="cardMessages[locale].more"
        icon="more_horiz" class="morehdr">
        <template #content>
          <div v-html="contentMore[locale]"></div>
        </template>
      </VaCollapse>

    </div>
   
    <div class="row">

      <VaSwitch v-if="controls.dataswitch" v-model="dataCtl" :label="cardMessages[locale].dstitle"
        :false-inner-label="cardMessages[locale].dsleft" :true-inner-label="cardMessages[locale].dsright"
        class="flex lg2 control switch" offColor="rgba(100,100,100,.4)" leftLabel />

        <VaSwitch v-if="controls.animate" 
           v-model="aniCtl" 
          :label="cardMessages[locale].animation" 
          :false-inner-label='cardMessages[locale].no'
          :true-inner-label='cardMessages[locale].yes'
          class="flex lg2 control switch"/>


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


    </div>

    <div class="chartpane">
      <!-- Chart component goes here -->
      <SimpleTree  v-if="chartValid"  :dataUrl="dataUrl" :dataName="dataName" 
      :ariaLabel="ariaLabel" :locale="chartLocale" 
      :dataProps="dataProps" @series="capture"></SimpleTree>
    </div>


    <div class="chartfooter">
      <!-- source, license, download button -->

      <VaChip disabled outline>
        {{ $t("license") }}: {{ dataLicense }}
      </VaChip>
      <!-- 
      <VaChip :href="dataUrl" target="_blank" >
        {{ $t("source") }}
      </VaChip>
      -->

      <VaButton round @click="jsonDown" icon="download" v-if="controls.downloads.data">
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
import { ref, onBeforeMount, nextTick, watch } from "vue";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import SimpleTree from "@/components/charts/SimpleTree.vue"
import html2canvas from 'html2canvas';

// for relocated base we need to prepend the base path to dynamic imports
const basePath = import.meta.env.BASE_URL

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

// needed to force re-render when dataurl reused
const chartValid = ref(true);

// content pane
const content = ref({});
const contentMore = ref({});
const showMore = ref(false);

const chartLocale = ref(locale);
const ariaLabel = ref("Aria TreeMap");

const dataCtl = ref(false);
const dataUrl = ref(null)
const dataName = ref(null)
const dataLicense = ref(null)
const dataProps = ref(null)

// controls
const controls = ref({
  range: false,
  dataswitch: false,
  downloads: { "data": true, "img": true },
  animate: false
})


const checkUrl = (url) => {
    // create new data uris here: use as is if starting with http else prepend base path
    if (url && url.toLowerCase().startsWith("http")) {
    return url
  } else {
    return basePath + url
  }
}

watch(locale, (lang) => {
  /*
  // console.log(props.name," - Locale:", lang, "index:", dataCtl.value ? 1 : 0);  
  dataName.value = cardMessages.value[lang].dsname[dataCtl.value ? 1 : 0] || "Data";
  // console.log("dsname:", dataName.value);
  ariaLabel.value = cardMessages.value[lang].aria + ": " + dataName.value
  */
  chartLocale.value = lang;
  updateData(0)
});


const mapData = ref(null)
const mapInstance = ref(null)

const capture = (data) => {
  console.log("Capture:", data)
  mapData.value = data.content
  mapInstance.value = data.chart
} 

const exportMap = async () => {
      if (mapInstance.value) {
        try {
          /*
          const panes = mapInstance.value.getPanes();
          panes.tilePane.style.zIndex = '1';    // Tiles should be at the bottom
          panes.overlayPane.style.zIndex = '2'; // Overlays (markers, etc.)
          panes.markerPane.style.zIndex = '3';  // Markers should be higher
          panes.popupPane.style.zIndex = '4';   // Popups and tooltips on top
          */
          const canvas = await html2canvas(mapInstance.value._container, {
            useCORS: true,
            allowTaint: true,
            backgroundColor: null,
            logging: false,
            scrollX: 0,
            scrollY: 0,
            width: mapInstance.value.offsetWidth,
            height: mapInstance.value.offsetHeight,
          });
          const imageUrl = await canvas.toDataURL('image/png');
          const filename = dataName.value + ".png";
          const link = document.createElement("a");
          link.href = imageUrl;
          link.download = filename;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        } catch (error) {
          console.error('Error exporting map:', error);
        }
      }
    };

const jsonDown = async () => {
  const data = JSON.stringify(mapData.value);
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${dataName.value}.json`
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};


const imgDown = () => {
  console.log("ImgDown:", mapInstance.value)
  if (!mapInstance.value) return;
  const imgUrl = mapInstance.value.getDataURL({
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
  console.log("DataCtl:", index)
  updateData(index ? 1 : 0);
  /*
  dataUrl.value = cardSpecs.value.data[dataCtl.value?1:0].url
  dataLicense.value = cardSpecs.value.data[dataCtl.value?1:0].license
  dataProps.value = cardSpecs.value.data[dataCtl.value?1:0].properties
  dataName.value = cardMessages.value[locale].dsname[dataCtl.value ? 1 : 0] || "Data";
  ariaLabel.value = cardMessages.value[locale].aria + ": " + dataName.value
  */
})

const updateData = async (index) => {
  const newUrl = checkUrl(cardSpecs.value.data[index].url);
  //console.log("UpdateData:", index, newUrl)
  if (newUrl === dataUrl.value) {
    chartValid.value = false;
    await nextTick();
  }
  dataUrl.value = newUrl;
  dataLicense.value = cardSpecs.value.data[index].license;
  dataProps.value = cardSpecs.value.data[index].properties;
  // name is localized!
  // dataName.value = cardSpecs.value.data[index].name || "Data"
  dataName.value = cardMessages.value[locale.value].dsname[index] || "Data";
  ariaLabel.value = cardMessages.value[locale.value].aria + ": " + dataName.value
  chartValid.value = true;
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
      noslider.value = cardSpecs.value.controls.range.noslider || false;
    }
    else {
      controls.value.range = false;
    }
    if (cardSpecs.value.controls.dataswitch.present && cardSpecs.value.data.length > 1)
      controls.value.dataswitch = cardSpecs.value.controls.dataswitch;
    else controls.value.dataswitch = false;

    if (cardSpecs.value.controls.animate.present)
      controls.value.animate = cardSpecs.value.controls.animate;
    else controls.value.animate = false;
    console.log("Ctls:", controls.value);
  }
  if (cardSpecs.value.controls.downloads !== undefined) {
    controls.value.downloads.img = cardSpecs.value.controls.downloads.image;
    controls.value.downloads.data = cardSpecs.value.controls.downloads.data;
  }
  await updateData(0);
  confgComplete.value = true
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

