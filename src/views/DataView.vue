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

// use anchor to give a unique reference to each tile
const tiles = [
  { "name": "DummyLine", "tag": "A", "anchor": "a1", "component": defineAsyncComponent(() => import("@/components/tiles/dummyLine/Card.vue")) },
  { "name": "DummyCustom", "tag": "B", "anchor": "a2", "component": defineAsyncComponent(() => import("@/components/tiles/dummyCustom/Card.vue")) },
  { "name": "DummyGraphics", "tag": "B", "anchor": "a3", "component": defineAsyncComponent(() => import("@/components/tiles/dummyGraphics/Card.vue")) },
  { "name": "DummyMap", "tag": "C", "anchor": "a4", "component": defineAsyncComponent(() => import("@/components/tiles/dummyMap/Card.vue")) }
]

const currentTags = ref(["A", "B", "C", "D", "E"])


const removeTag = (tag) => {
  currentTags.value = currentTags.value.filter(item => item !== tag);
}
const insertTag = (tag) => {
  // make sure we donÄt get duplicates
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
