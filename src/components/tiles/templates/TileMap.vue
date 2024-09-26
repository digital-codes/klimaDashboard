<template>
  <div class="card">
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
      <SimpleMap :dataUrl="dataUrl" :dataName="dataName" 
      :ariaLabel="ariaLabel" :locale="chartLocale" 
      :dataProps="dataProps" @data="capture"></SimpleMap>
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

      <VaButton round @click="csvDown" icon="download" v-if="controls.downloads.data">
        {{ cardMessages[locale].download }}
      </VaButton>

      <VaButton round @click="imgDown" icon="download" v-if="controls.downloads.img">
        {{ cardMessages[locale].downimage }}
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

import SimpleMap from "@/components/charts/SimpleMap.vue"
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

// content pane
const content = ref({});
const contentMore = ref({});
const showMore = ref(false);

const chartLocale = ref(locale);
const ariaLabel = ref("Aria TileMap");

const dataCtl = ref(false);
const dataUrl = ref(null)
const dataName = ref(null)
const dataLicense = ref(null)

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
  // console.log(props.name," - Locale:", lang, "index:", dataCtl.value ? 1 : 0);
  dataName.value = cardMessages.value[lang].dsname[dataCtl.value ? 1 : 0] || "Data";
  // console.log("dsname:", dataName.value);
  ariaLabel.value = cardMessages.value[lang].aria + ": " + dataName.value
  chartLocale.value = lang;
  // updateData(0)
});


const mapData = ref(null)
const mapInstance = ref(null)

const capture = (data) => {
  mapData.value = data.content
  mapInstance.value = data.map
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

const downJson = async () => {
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

watch(dataCtl, (index) => {
  console.log("DataCtl:", index)
  dataUrl.value = cardMessages.specs.data[dataCtl.value?1:0].url
  dataLicense.value = cardMessages.specs.data[dataCtl.value?1:0].license
})


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

    if (cardSpecs.value.controls.stacked.present)
      controls.value.stacked = cardSpecs.value.controls.stacked;
    else controls.value.stacked = false;
    if (cardSpecs.value.controls.animate.present)
      controls.value.animate = cardSpecs.value.controls.animate;
    else controls.value.animate = false;
    console.log("Ctls:", controls.value);
  }
  if (cardSpecs.value.controls.downloads !== undefined) {
    controls.value.downloads.img = cardSpecs.value.controls.downloads.image;
    controls.value.downloads.data = cardSpecs.value.controls.downloads.data;
  }

  confgComplete.value = true
  // updateData(0);
});

</script>

<style scoped lang="scss">

@import '@/style/colors.scss';

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
  border-color: light-dark($dash-border-light, $dash-border-dark) !important;
  border:1px solid;
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


<style lang="scss" scoped>

@import "vuestic-ui/styles/grid";

</style>

