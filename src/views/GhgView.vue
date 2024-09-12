<template>

  <HeaderCard name="header" @filter="filterTag" id="dh" />

  <div v-for="(tile, index) in tiles" :key="index" :id="tile.anchor">
    <component v-if="currentTags.includes(tile.tag)" :is="tile.component" :name="tile.name" :prefix="tile.prefix" class="tile">
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
// using template for linebar. maybe still loads component multiple times. ptah prefix needed for dynamic import with template
{ "name": "KskKa_d_energy", "prefix":"../protect/actions","tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
{ "name": "KskKa_d_ghg", "prefix":"../protect/thg","tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
{ "name": "KskKa_d_stwkenergy", "prefix":"../protect/actions","tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },

{ "name": "DummyTable", "tag": "D", "component": defineAsyncComponent(() => import("@/components/tiles/test/dummyTable/Card.vue")) },
{ "name": "DummyGraphics", "tag": "B",  "component": defineAsyncComponent(() => import("@/components/tiles/test/dummyGraphics/Card.vue")) },
// { "name": "DummyGauge", "tag": "D",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyGauge/Card.vue")) },
{ "name": "DummyMap", "tag": "C",  "component": defineAsyncComponent(() => import("@/components/tiles/test/dummyMap/Card.vue")) }
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
