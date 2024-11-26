<template>

  <HeaderCard name="weather" @filter="filterTag" id="dh" :icons="[icon_l, icon_d]" />

  <div v-for="(tile, index) in tiles" :key="index" :id="tile.anchor">
    <component v-if="currentTags.includes(tile.tag)" :is="tile.component" :name="tile.name" :section="tile.section"
      :part="tile.part" class="tile">
    </component>
  </div>

</template>

<script setup>
// 1i8n at top !
import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales } = useI18n();

import { ref, watch, onMounted, computed } from 'vue';
import { defineAsyncComponent } from 'vue'

// special header for the datavies
const HeaderCard = defineAsyncComponent(() => import("@/components/header/Card.vue"))

import icon_l from "@/assets/icons/dashboard/weather.svg?url"
import icon_d from "@/assets/icons/dashboard/weather_d.svg?url"


const tiles = [
  // using template for linebar. maybe still loads component multiple times. need section and part for dynamic import with template
  // final import from ../<section>/<part>/<name>/
    { "name": "esriPois", "section": "conditions", "part": "weather", "tag": "B", "component": defineAsyncComponent(() => import("@/components/tiles/templates/VectorMap.vue")) },
    //{ "name": "KaWeather", "section": "", "part": "", "tag": "A", "component": defineAsyncComponent(() => import("@/components/tiles/conditions/weather/current/Card.vue")) },
  //{ "name": "pois", "section": "conditions", "part": "weather", "tag": "B", "component": defineAsyncComponent(() => import("@/components/tiles/templates/TileMap.vue")) },
]

// use anchor to give a unique reference to each tile
tiles.map(tile => {
  tile.anchor = tile.name
  console.log("Tile:", tile.name, tile.tag, tile.anchor)
})

const currentTags = ref(["A", "B", "C", "D", "E"])


const removeTag = (tag) => {
  currentTags.value = currentTags.value.filter(item => item !== tag);
}
const insertTag = (tag) => {
  // make sure we don't get duplicates
  currentTags.value = currentTags.value.filter(item => item !== tag);
  currentTags.value.push(tag)
}

const filterTag = (tag) => {
  if (currentTags.value.includes(tag)) {
    removeTag(tag)
  } else {
    insertTag(tag)
  }
}


</script>
