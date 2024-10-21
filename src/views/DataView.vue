<template>

  <HeaderCard name="test" @filter="filterTag" id="dh" />

      <div v-if="tilesVisible > 0">
        <div v-for="(tile, index) in tileList" :key="index" :id="tile.anchor">
          <component v-if="currentTags.includes(tile.tag)" :is="tile.component" :name="tile.name" :section="tile.section"
            :part="tile.part" class="tile">
          </component>
        </div>
      </div>

      <div v-if="tilesVisible < tiles.length">
        <VaButton @click="appendTiles" class="btt-button" :aria-label="$t('continue')"
          >
          <VaIcon name="keyboard_arrow_down" size="medium" />{{ $t('continue') }}
        </VaButton>
      </div>


</template>

<script setup>
// 1i8n at top !
import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales } = useI18n();

import { ref, onMounted, nextTick } from 'vue';
import { defineAsyncComponent } from 'vue'
import { VaButton } from 'vuestic-ui';

// special header for the datavies
const HeaderCard = defineAsyncComponent(() => import("@/components/header/Card.vue"))

// reactive structue to enable something like infinitescroll, as vaInfiniteScroll is not working
// with cards (?)
const scrollTarget = ref(null)
const tileList = ref([])
const tilesVisible = ref(0)
const appendTiles = async () => {
  if (tilesVisible.value < tiles.length) {
    tileList.value.push(tiles[tilesVisible.value]);
    tilesVisible.value += 1
  }
}

const tiles = [
  // using template for linebar. maybe still loads component multiple times. 
  { "name": "test1", "section": "test", "part": "dummyTree", "tag": "A", "component": defineAsyncComponent(() => import("@/components/tiles/templates/TreeMap.vue")) },
//  { "name": "test1", "section": "test", "part": "dummyTable", "tag": "A", "component": defineAsyncComponent(() => import("@/components/tiles/templates/DataTable.vue")) },
  { "name": "energyQuarters", "section": "conditions", "part": "statistics", "tag": "E", "component": defineAsyncComponent(() => import("@/components/tiles/templates/ChoroMap.vue")) },
  { "name": "byProgress", "section": "protect", "part": "status", "tag": "C", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
  //{ "name": "DummyLineCjs", "section": "dummyLineCjs", "part": ".", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/test/dummyLineCjs/Card.vue")) },
  //{ "name": "DummyLineApx", "tag": "A",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyLineApx/Card.vue")) },
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

onMounted(async () => {
  // Code to execute when the component is mounted
  console.log('mounted')
  await appendTiles()
  await nextTick()
})

</script>
