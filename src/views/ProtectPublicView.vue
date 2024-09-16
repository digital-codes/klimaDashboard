<template>

  <HeaderCard name="protpub" @filter="filterTag" id="dh"  :icons="[icon_l, icon_d]"/>

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
import icon_l from "@/assets/icons/dashboard/protection.svg?url"
import icon_d from "@/assets/icons/dashboard/protection_d.svg?url"

const tiles = [
  // using template for linebar. maybe still loads component multiple times. need section and part for dynamic import with template
  // final import from ../<section>/<part>/<name>/
  { "name": "KskKa_d_energy", "section": "protect", "part": "actions", "tag": "A", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
  { "name": "KskKa_d_ghg", "section": "protect", "part": "thg", "tag": "A", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
  { "name": "KskKa_d_stwkenergy", "section": "protect", "part": "actions", "tag": "A", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
  { "name": "renewableShare", "section": "conditions", "part": "energyCharts", "tag": "B", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
  // { "name": "DummyGauge", "tag": "D",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyGauge/Card.vue")) },
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
