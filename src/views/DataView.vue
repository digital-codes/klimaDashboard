<template>

  <HeaderCard name="header" @filter="filterTag" id="dh" />

  <div v-for="(tile, index) in tiles" :key="index" :id="tile.anchor">
    <component v-if="currentTags.includes(tile.tag)" :is="tile.component" :name="tile.name" class="tile">
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

const tiles = [
// using template for linebar. maybe still loads component multiple times. 
//{ "name": "KskKaEnergy", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/KskKa_d_energy/Card.vue")) },
//{ "name": "KskKaGhg", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/KskKa_d_ghg/Card.vue")) },
//{ "name": "DummyLine", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyLine/Card.vue")) },
{ "name": "KaWeather", "tag": "E",  "component": defineAsyncComponent(() => import("@/components/tiles/weatherDisplay/Card.vue")) },
{ "name": "KskKa_d_energy", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
{ "name": "KskKa_d_ghg", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
{ "name": "KskKa_d_stwkenergy", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
//{ "name": "dummyLine", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
//{ "name": "DummyLineCjs", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyLineCjs/Card.vue")) },
//{ "name": "DummyLineApx", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyLineApx/Card.vue")) },
//  { "name": "DummyCustom", "tag": "B", "component": defineAsyncComponent(() => import("@/components/tiles/dummyCustom/Card.vue")) },
{ "name": "DummyTable", "tag": "D", "component": defineAsyncComponent(() => import("@/components/tiles/dummyTable/Card.vue")) },
{ "name": "DummyGraphics", "tag": "B",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyGraphics/Card.vue")) },
// { "name": "DummyGauge", "tag": "D",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyGauge/Card.vue")) },
{ "name": "DummyMap", "tag": "C",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyMap/Card.vue")) }
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
