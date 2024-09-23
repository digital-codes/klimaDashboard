<script setup>
import { ref, onMounted, watch, onUnmounted } from "vue";
import { nextTick } from "vue";

import VChart, { UPDATE_OPTIONS_KEY } from "vue-echarts";
import { registerMap } from "echarts";

import { useConfigStore } from "@/services/configStore";
const configStore = useConfigStore();

// breakpoint
import { useBreakpoint } from "vuestic-ui";
const breakpoint = useBreakpoint();

// geojson
// geoUrl = "/data/karlsruhe/ka.geojson"
const geoUrl = "https://transparenz.karlsruhe.de/dataset/8474ba52-f851-4f4b-b05a-1cba9bbd1f4d/resource/2a7fd644-bc67-477a-bb9e-cf88f076b7af/download/stadtteile.json"

const kaData = [
    {"name": "Innenstadt-Ost", "value": 7},
    {"name": "Innenstadt-West", "value": 71},
    {"name": "Suedstadt", "value": 19}, 
    {"name": "Suedweststadt", "value": 23},
    {"name": "Weststadt", "value": 47},
    {"name": "Nordweststadt", "value": 40},
    {"name": "Oststadt", "value": 1},
    {"name": "Muehlburg", "value": 5},
    {"name": "Daxlanden", "value": 9},
    {"name": "Knielingen", "value": 9},
    {"name": "Gruenwinkel", "value": 52},
    {"name": "Oberreut", "value": 52},
    {"name": "Beiertheim-Bulach", "value": 63},
    {"name": "Weiherfeld-Dammerstock", "value": 75},
    {"name": "Rueppurr", "value": 90},
    {"name": "Waldstadt", "value": 88},
    {"name": "Rintheim", "value": 25},
    {"name": "Hagsfeld", "value": 11}, 
    {"name": "Durlach", "value": 66}, 
    {"name": "Groetzingen", "value": 76}, 
    {"name": "Stupferich", "value": 56},
    {"name": "Hohenwettersbach", "value": 71},
    {"name": "Wolfartsweier", "value": 14}, 
    {"name": "Gruenwettersbach", "value": 78}, 
    {"name": "Palmbach", "value": 33},
    {"name": "Neureut", "value": 77},
    {"name": "Nordstadt", "value": 96}
]

const chartOptions = ref(
  {
    title: {
      text: 'Karslruhe Klimadash',
      subtext: 'SUbtext',
      sublink: 'SubLink',
      left: 'right'
    },
    tooltip: {
      trigger: 'item',
      showDelay: 0,
      transitionDuration: 0.2
    },
    visualMap: {
      left: 'right',
      min: 20,
      max: 50,
      inRange: {
        color: [
          '#313695',
          '#4575b4',
          '#74add1',
          '#abd9e9',
          '#e0f3f8',
          '#ffffbf',
          '#fee090',
          '#fdae61',
          '#f46d43',
          '#d73027',
          '#a50026'
        ]
      },
      text: ['High', 'Low'],
      calculable: true
    },
    toolbox: {
      show: true,
      //orient: 'vertical',
      left: 'left',
      top: 'top',
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {}
      }
    },
    series: [
      {
        name: 'Karlsruhe Energiequartiere',
        type: 'map',
        roam: true,
        map: 'KA',
        emphasis: {
          label: {
            show: true
          }
        },
        // data: kaData // []
        data: [
        {"name": "Weststadt", "value": 47}
        ]
      }
    ]
  })


// import composables


import { use } from "echarts/core";
import { SVGRenderer, CanvasRenderer } from "echarts/renderers";
// normally, only a single chart type is needed
// unless toolbox allows to switch types (like here ...)
import { LineChart, BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";

// optimize later
// import "echarts"

import { useColors } from "vuestic-ui";
const { currentPresetName } = useColors();

const emit = defineEmits(["series"]);

const props = defineProps({
  /* Add your props here */
  dataUrl: {
    type: String,
    required: true,
  },
  polyUrl: {
    type: String,
    required: true,
  },
  // the field name we are looking for
  polyId: {
    type: String,
    default: "name",
  },
  // value feature
  featureName: {
    type: String,
    default: "value",
  },
  dataName: {
    type: String,
    default: "LineChart",
  },
  ariaLabel: {
    type: String,
    default: "Aria LineChart",
  },
  locale: {
    type: String,
    default: "de",
  }
});

const theChart = ref(null);
const chartTheme = ref(currentPresetName); // already reactive. don't watch for theme
const dataLoaded = ref(false);
const data = ref(null);
const datakeys = ref(null);
const ariaLabel = ref(props.ariaLabel);

const animTimer = ref(null);
const fullXRange = ref({});
const fullData = ref([]);

watch(currentPresetName, (newValue, oldValue) => {
  console.log("Theme changed:", newValue);
  chartTheme.value = newValue;
  if (newValue == "dark") {
    for (let i = 0; i < chartOptions.value.series.length; i++) {
      chartOptions.value.series[i].label.color = "white";
    }
  } else {
    for (let i = 0; i < chartOptions.value.series.length; i++) {
      chartOptions.value.series[i].label.color = "black";
    }
  }
});


watch(
  () => props.locale,
  (newValue, oldValue) => {
    //console.log("Type changed:", newValue);
    updateOptions();
  }
);


watch(
  () => props.ariaLabel,
  (newValue, oldValue) => {
    //console.log("Type changed:", newValue);
    ariaLabel.value = props.ariaLabel;
  }
);


watch(
  () => props.dataName,
  async (newValue, oldValue) => {
    // update title
    chartOptions.value.title.text = props.dataName;
  }
);


const getDataRange = () => {
  // animation range
  const mxData = [];
  const mnData = [];
  for (const series of chartOptions.value.series) {
    const mx = Math.max(...series.data);
    mxData.push(mx);
    const mn = Math.min(...series.data);
    mnData.push(mn);
  }
  /*
  let mx;
  mx = props.stacked
    ? mxData.reduce((acc, cur) => acc + cur, 0)
    : Math.max(...mxData);

  if (mx > 100) mx = Math.ceil(1.05 * mx);
  else mx += 2;
  */
  const range = { min: Math.min(...mnData), max: Math.max(...mxData), smax: mxData.reduce((acc, cur) => acc + cur, 0) }
  console.log("Range:", range);
  return range
};

const saveData = () => {
  // save data 
  fullData.value = JSON.parse(JSON.stringify(chartOptions.value.series));
  // max data values
  const range = getDataRange();
  // and X range
  fullXRange.value = {
    idx: 0,
    len: chartOptions.value.xAxis.data.length,
    range: JSON.parse(JSON.stringify(chartOptions.value.xAxis.data)),
    max: range.max,
    smax: range.smax
  };
  console.log("Range value max:", fullXRange.value.max);
}

const setupXRange = () => {
  let mx = props.stacked ? fullXRange.value.smax : fullXRange.value.max;
  if (mx > 100) mx = Math.ceil(1.05 * mx);
  else mx += 2;
  chartOptions.value.yAxis.max = mx
};



const updateOptions = async () => {
  const size = breakpoint.smUp ? "large" : "small";
  console.log("Size:", size);
  return
  chartOptions.value = await updateEchartsOptions(
    chartOptions.value,
    data.value,
    props.dataX,
    props.dataClasses,
    props.dataColumns,
    props.type,
    props.stacked,
    size,
    props.locale
  );
};

const theMap = ref(null);
const loadData = async () => {
  console.log("Loading polygons from : ", props.polyUrl);
  try {
    const response = await fetch(props.polyUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const geoData = await response.json();
    const features = geoData.features;
    // ka geojson has property NAME. We need name
    for (const item of features) {
      item.properties.name = item.properties.NAME.replace("ü","ue").replace("ö","oe").replace("ä","ae")
    }
    theMap.value = registerMap('KA', {geoJSON: geoData})
    dataLoaded.value = true;
    await nextTick();
    // emit data after data loaded, else chart intance is not ready
    emit("series", {},theChart.value);
  } catch (error) {
    console.error("Failed to load polygon data:", error);
    return
  }    
  try {
    // load data into chart
    console.log("Loading data from : ", props.dataUrl);
    const response = await fetch(props.dataUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const chartValues = await response.json();
    chartOptions.value.series[0].data = chartValues
  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
  return
  try {
    console.log("Fetching: ", props.dataUrl);
    const response = await fetch(props.dataUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    datakeys.value = [];
    if (props.dataFormat == "json") {
      data.value = await response.json();
      //console.log("JSON:", data.value);
    } else {
      // assume csv
      const csvString = await response.text();
      //console.log("raw CSV:",csvString)
      Papa.parse(csvString, {
        header: true,
        dynamicTyping: true,
        complete: async function (results) {
          // console.log("CSV parsed:", results.data);
          data.value = results.data;
        },
      });
    }
    //if (theChart.value) await theChart.value.setOption(chartOptions.value, true, true);
    if (theChart.value) await theChart.value.clear();
    await updateOptions();
    await nextTick();

    // save data from xrange and animation
    saveData()
    // emit limits
    const yrange = getDataRange();
    console.log("Emitting y range",yrange);
    emit("yrange", [yrange.min, yrange.max]);
    const xrange = chartOptions.value.xAxis.data
    console.log("Emitting x range",xrange);
    emit("xrange", [xrange[0], xrange[xrange.length - 1]])
    dataLoaded.value = true;
    await nextTick();
    // emit data after data loaded, else chart intance is not ready
    emit("series", {"x":chartOptions.value.xAxis.data,"cols":fullData.value, "chart":theChart.value},theChart.value);
  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
};

use([
  CanvasRenderer,
  SVGRenderer,
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
]);

/*
const chartOptions = ref(
  lineBarDefaults(
    props.dataName,
    props.labelX,
    props.labelY,
    breakpoint.smUp ? "large" : "small",
    props.locale
  )
);
*/


onMounted(async () => {
  if (configStore.getTheme == "dark") {
    console.log("Dark theme detected");
  } else {
    console.log("Light theme detected");
  }

  await loadData();
});

onUnmounted(() => {
  if (animTimer.value) {
    clearInterval(animTimer.value);
  }
});
</script>

<template>
  <v-chart v-if="dataLoaded" ref="theChart" :option="chartOptions" :style="{ height: '100%' }" :theme="chartTheme"
    :init-options="{ renderer: 'canvas' }" autoresize :aria-label="ariaLabel" @ready="onChartReady">
  </v-chart>
</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
