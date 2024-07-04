<script setup>
import { ref, onMounted, watch } from "vue";
import { nextTick } from 'vue';

import VChart, { UPDATE_OPTIONS_KEY } from "vue-echarts";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

// import composables
import { lineBarDefaults, updateEchartsOptions } from '@/composables/EchartsUtils';


// data parser
import Papa from 'papaparse';
// https://www.data-forge-js.com/
// https://github.com/data-forge/data-forge-ts/blob/master/docs/guide.md

import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
// normally, only a single chart type is needed
// unless toolbox allows to switch types (like here ...)
import { LineChart, BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent
} from "echarts/components";

// optimize later
// import "echarts"

import { useColors } from "vuestic-ui";
const { currentPresetName } = useColors();

const props = defineProps({
  /* Add your props here */
  dataUrl: {
    type: String,
    required: true,
  },
  dataName: {
    type: String,
    default: "LineChart",
  },
  // optional X axis identifier
  dataX: {
    type: String,
    default: "",
  },
  // optional Y axis identifier
  dataY: {
    type: String,
    default: "",
  },
  // optional format
  dataFormat: {
    type: String,
    default: "json",
  },
  // optional columns to be selected
  dataColumns: {
    type: Array,
    default: [],
  },
  // optional classes to be selected
  dataClasses: {
    type: Array,
    default: [],
  },
  // optional index.
  dataIdx: {
    type: Number,
    default: 0
  },
  type: {
    type: String,
    default: "line"
  },
  stacked: {
    type: Boolean,
    default: false
  },
  range: {
    type: Number,
    default: 50
  },
  animate: {
    type: Boolean,
    default: false
  },
});

const theChart = ref(null);
const chartTheme = ref(currentPresetName) // already reactive. don't watch for theme
const dataLoaded = ref(false);
const data = ref(null);
const datakeys = ref(null);

watch(currentPresetName, (newValue, oldValue) => {
  console.log("Theme changed:", newValue);
  chartTheme.value = newValue;
});

watch(currentPresetName, (newValue, oldValue) => {
  if (newValue == "dark") {
    for (let i = 0; i < chartOptions.value.series.length; i++) {
      chartOptions.value.series[i].label.color = "white"
    }
  } else {
    for (let i = 0; i < chartOptions.value.series.length; i++) {
      chartOptions.value.series[i].label.color = "black"
    }
  }
});



watch(() => props.type, (newValue, oldValue) => {
  console.log("Type changed:", newValue);
  updateOptions()
});

watch(() => props.stacked, (newValue, oldValue) => {
  console.log("Stacked changed:", newValue);
  updateOptions()
});


watch(() => props.range, (newValue, oldValue) => {
  console.log("Range changed:", newValue);
});

watch(() => props.dataUrl, async (newValue, oldValue) => {
  console.log("Data URL changed:", newValue);
  if (theChart.value) await theChart.value.clear()
  await loadData();
  // also update title
  chartOptions.value.title.text = props.dataName

});

watch(() => props.animate, (newValue, oldValue) => {
  console.log("Animate changed:", newValue);
});


const updateOptions = async () => {
  chartOptions.value = await updateEchartsOptions(chartOptions.value, 
    data.value, props.dataX, props.dataClasses, props.dataColumns, props.type, props.stacked)
}

const loadData = async () => {
  try {
    console.log("Fetching: ", props.dataUrl);
    const response = await fetch(props.dataUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    datakeys.value = []
    if (props.dataFormat == "json") {
      data.value = await response.json();
      //console.log("JSON:", data.value);
      await updateOptions()
    } else { // assume csv
      const csvString = await response.text();
      //console.log("raw CSV:",csvString)
      Papa.parse(csvString, {
        header: true,
        dynamicTyping: true,
        complete: async function (results) {
          //console.log("CSV parsed:", results.data);
          data.value = results.data;
          await updateOptions()
        }
      });
    }
    await nextTick();
    dataLoaded.value = true;
  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
}

use([
  CanvasRenderer,
  LineChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent
]);

const chartOptions = ref(lineBarDefaults(props.dataName))


onMounted(async () => {

  if (configStore.getTheme == "dark") {
    console.log("Dark theme detected")
  } else {
    console.log("Light theme detected")
  }

  await loadData();

});
</script>

<template>
  <v-chart v-if="dataLoaded" ref="theChart" :option="chartOptions" :style="{ height: '100%' }" :theme="chartTheme"
    autoresize></v-chart>
</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
