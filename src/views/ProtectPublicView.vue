<template>

  <HeaderCard name="protpub" @filter="filterTag" id="dh" :icons="[icon_l, icon_d]" />
<!-- -->
  <div v-if="tilesCompleted" v-for="(tile, index) in tiles" :key="index" :id="tile.anchor">
    <component v-if="currentTags.includes(tile.tag)" :is="tile.component" :name="tile.name" :section="tile.section"
      :part="tile.part" class="tile">
    </component>
  </div>
  <!-- -->
  <!-- 
  <div v-if="tilesCompleted" v-for="(tile, index) in tiles" :key="index" :id="tile.anchor">
    <div v-if="currentTags.includes(tile.tag)" >
      <component v-if="tile.type == 'template'" :is="tile.component" :name="tile.name" :section="tile.section"
      :part="tile.part" class="tile">
    </component>
    <component v-else :is="tile.component" :name="tile.name" class="tile">
    </component>
    </div>
  </div>
  -->

</template>

<script setup>
// 1i8n at top !
import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales } = useI18n();

import { ref, shallowRef, watch, onMounted, computed, onBeforeMount } from 'vue';
import { defineAsyncComponent } from 'vue'

// special header for the datavies
const HeaderCard = defineAsyncComponent(() => import("@/components/header/Card.vue"))
import icon_l from "@/assets/icons/dashboard/protection.svg?url"
import icon_d from "@/assets/icons/dashboard/protection_d.svg?url"

import TimeLine from "@/components/tiles/templates/TimeLine.vue"
import LineBar from "@/components/tiles/templates/LineBar.vue"
import DataTable from "@/components/tiles/templates/DataTable.vue"
import DummyGauge from "@/components/tiles/test/dummyGauge/Card.vue"
const comps = { "LineBar": LineBar, "DummyGauge": DummyGauge, "DataTable": DataTable, "TimeLine": TimeLine }


const tilesCompleted = ref(false)
// import tiles from "./configs/PublicProtectTiles.json"
import tileConfig from "@/views/configs/ProtectPublic.json"

const tiles = shallowRef([])
/*
const tiles = [
  // using template for linebar. maybe still loads component multiple times. need section and part for dynamic import with template
  // final import from ../<section>/<part>/<name>/
    { "name": "a2_1_fernwaerme", "section": "protect", "part": "actions", "tag": "A", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
    { "name": "KskKa_d_energy", "section": "protect", "part": "actions", "tag": "B", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
    { "name": "KskKa_d_ghg", "section": "protect", "part": "thg", "tag": "B", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
  { "name": "KskKa_d_stwkenergy", "section": "protect", "part": "actions", "tag": "B", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
  { "name": "renewableShare", "section": "conditions", "part": "energyCharts", "tag": "B", "component": defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue")) },
  // { "name": "DummyGauge", "tag": "D",  "component": defineAsyncComponent(() => import("@/components/tiles/dummyGauge/Card.vue")) },
]
*/

// const currentTags = ref(["A", "B", "C", "D", "E"])
const currentTags = ref([])

// use anchor to give a unique reference to each tile
tileConfig.map(tile => {
  tile.anchor = tile.name
  console.log("Tile:", tile.name, tile.tag, tile.anchor)
  if (!currentTags.value.includes(tile.tag)) {
    console.log("Add Tag:", tile.tag)
    currentTags.value.push(tile.tag)
  }
})

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

onBeforeMount(async () => {
  for (const tile of tileConfig) {
    tile.anchor = tile.name
    // specs can indicate template or custom component with name
    // custom could go without props but semm to work with template props as well ...
    // alternative is to not use dynamic imports but have all components in the bundle
    const useDynamic = false
    if (tile.specs.hasOwnProperty("template")) {
      console.log("Template:", tile.specs.template)
      if (useDynamic) {
        // we need literal strings for dynamic imports. use switch statement
        switch (tile.specs.template) {
          case "LineBar":
            tile.component = defineAsyncComponent(() => import("@/components/tiles/templates/LineBar.vue"))
            break
            case "DataTable":
            tile.component = defineAsyncComponent(() => import("@/components/tiles/templates/DataTable.vue"))
            break
            case "ChoroMap":
            tile.component = defineAsyncComponent(() => import("@/components/tiles/templates/ChoroMap.vue"))
            break
            case "TileMap":
            tile.component = defineAsyncComponent(() => import("@/components/tiles/templates/TileMap.vue"))
            break
            default:
              alert("Unknown template:" + tile.specs.template)
        }
      } else {
        tile.component = comps[tile.specs.template]
      }
      tile.type = "template"
    } else {
      console.log("Plain Comp:", tile.specs)
      tile.component = comps[tile.specs.name]
      tile.type = "custom"
    }
    tiles.value.push(tile)
  }
  console.log("Tiles:", tiles.value)
  tilesCompleted.value = true
})


</script>
