<template>
  <VaCard class="headerCard" ref="theCard"  v-if="confgComplete">
    <!-- 
    <div>
      <VaAvatar title="Klima Dashboard" :src="modeSwitch == 'dark' ? climate_d : climate_l" :size="breakpoint.smUp ? 'medium' : 'small'" />
      <h1 class="headertitle" :class="breakpoint.xs ? 'headertitlesm' : 'xy'">{{ $t($props.name + ".title") }}</h1>
    </div>

    -->

    <div class="dataheader">
      <VaAvatar title="Klima Dashboard" :src="modeSwitch == 'dark' ? props.icons[1] : props.icons[0]" size="3rem" />
      <h1 class="headertitle" :class="breakpoint.xs ? 'headertitlesm' : ''">{{  cardMessages[locale].title }}</h1>
    </div>
    <!--
    <FilterInfo :name="infoName" :content="infoContent" :link="infoLink" :img="infoImg" :open="infoOpen" @close="infoOpen=false"/>
    -->


    <!-- 
    <p class="headertext">{{ $t($props.name + ".text") }}</p>
    -->

    <div class="flex xs12 mdcontent">
      <div v-html="content[locale]"></div>
      <div v-if="controls.detail.present" style="text-align:left;margin:1rem 0 1rem 0;">
        <VaButton @click="showDetails" icon="more_horiz" color="primary" size="small" round>
        {{ $t("more") }}
      </VaButton>
      </div>
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
        :label="cardMessages[locale][filter.label]" right-label @input="action(filter.name)" >
        <template #innerLabel>
          <div class="va-text-center">
            <VaIcon :name="filter.icon" />
          </div>
        </template>
        </VaSwitch>
      </div>
    </div>

    <div class="filterInfo" ref="filterPane" style="scroll-margin-top: 8rem;">
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

import { useRouter } from 'vue-router';
const router = useRouter();

import FilterInfo from "@/components/pops/FilterInfo.vue";
const infoName = ref("Infoname")
const infoContent = ref("")
const infoOpen = ref(false)
const infoLink = ref("")
const infoImg = ref(null)

const breakpoint = useBreakpoint();

const theCard = ref(null);
const filterPane = ref(null);

const cardMessages = ref({});
const cardSpecs = ref({});
const confgComplete = ref(false);
// content pane
const content = ref({});

// controls
const controls = ref({
  detail: { "present": false, "name": "" }
});


// mode switch 
import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();
const modeSwitch = ref("light")

watch(() => configStore.getTheme, (newVal, oldVal) => {
  console.log("Mode switch1:", newVal)
  modeSwitch.value = configStore.getTheme
})

const showDetails = () => {
  console.log("Show Details:", controls.value.detail.name);
  router.push({ name: "Detail", params: { topic: controls.value.detail.name } });
};


const filters = ref([
]);


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


import { loadMsgs, loadText, loadSpecs } from "@/composables/LoadSpecs"

const infoTag = ref(-1)

const infoAction = async (tag) => {
  console.log("Info action:", tag)
  if (infoOpen.value && (infoTag.value == tag)) {
  //if (infoOpen.value) {
      infoOpen.value = false
  } else {
    infoTag.value = tag
    // console.log("Info action:", tag)
    infoName.value = cardMessages.value[locale.value][filters.value[tag].label]
    infoContent.value = filters.value[tag].content || "No content defined"
    infoLink.value = filters.value[tag].link
    infoImg.value = filters.value[tag].img || null
    infoOpen.value = true
    if (breakpoint.smDown) {
      nextTick(() => {
        // make sureto have scroll-margin set in style
        filterPane.value.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
  }
}

onBeforeMount(async () => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  // localized content
  const supportedLanguages = configStore.getLanguages;

  const cardContent = await loadText(props, supportedLanguages, "hdr")
  cardMessages.value = await loadMsgs(props, supportedLanguages, "hdr")
  cardSpecs.value = await loadSpecs(props, "hdr")

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;

    let updatedContent = cardContent[key];
    content.value[key] = updatedContent;
  }

  modeSwitch.value = configStore.getTheme

  // filters, optional
  if (cardSpecs.value.filters) {
    filters.value = cardSpecs.value.filters
  }
  if (cardSpecs.value.detail !== undefined) {
    console.log("Detail:", cardSpecs.value.detail);
    controls.value.detail.present = true
    controls.value.detail.name = cardSpecs.value.detail.name
  }

  confgComplete.value = true

});
</script>


<style scoped lang="scss">
@use "sass:color";
@use '@/style/colors.scss';
@use "vuestic-ui/styles/grid";

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

.infoicon  {
  margin-left: 0;
  margin-right: .5rem;
  --va-background-color: unset  !important;
}

button.infoicon {
  padding:0;
  vertical-align: middle;
}


.infoicon :deep(i) {
  color: light-dark(colors.$dash-accent-light, colors.$dash-accent-dark)!important;
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
