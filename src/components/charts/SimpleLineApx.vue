<script setup>
import { ref, onMounted, watch } from "vue";
import { nextTick } from "vue";

import { useConfigStore } from "@/services/configStore";
const configStore = useConfigStore();

// import composables
import getDataSymbol from "@/composables/DataSymbol";

// data parser
import Papa from "papaparse";
// https://www.data-forge-js.com/
// https://github.com/data-forge/data-forge-ts/blob/master/docs/guide.md
import * as dataForge from "data-forge";

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
    default: 0,
  },
  type: {
    type: String,
    default: "line",
  },
  stacked: {
    type: Boolean,
    default: false,
  },
  range: {
    type: Number,
    default: 50,
  },
  animate: {
    type: Boolean,
    default: false,
  },
});

const theChart = ref(null);
const chartTheme = ref(currentPresetName); // already reactive. don't watch for theme
const dataLoaded = ref(false);
const data = ref(null);
const datakeys = ref(null);
const chartType = ref("line");

const chartData = ref([
{
    name: "High - 2013",
    data: [28, 29, 33, 36, 32, 32, 33],
  },
  {
    name: "Low - 2013",
    data: [12, 11, 14, 18, 17, 13, 13],
  },
  {
    name: "High - 2013",
    data: [18, 39, 13, 6, 3, 30, 35],
  },
]);

const dataColor = ref([]);
const dataSymbol = ref([]);
const dataSymbolSize = ref([]);
const dataDash = ref([]);
const dataPattern = ref([])

const chartOptions = ref({
  // apexcharts
  chart: {
    //height: 350,
    //height:"100%",
    //width:"100%",
    type: "line",
    dropShadow: {
      enabled: true,
      color: "#000",
      top: 18,
      left: 7,
      blur: 10,
      opacity: 0.2,
    },
    zoom: {
      enabled: false,
    },
    toolbar: {
      show: false,
    },
  },
  colors: dataColor.value,
  stroke: {
    width: 2,
    curve: "straight",
    dashArray: dataDash.value,
    //curve: "smooth",
  },
  fill: {
              type: 'pattern',
              opacity: 1,
              pattern: {
                style: dataPattern.value, // string or array of strings
              },
            },
  markers: {
    shape: dataSymbol.value, //"circle", //"circle" or square,
    radius: 0, // don't use on square ... rounded corner
    size: dataSymbolSize.value,
  },
  dataLabels: {
    enabled: true,
    offsetX: 10,
  },
  title: {
    text: "Average High & Low Temperature",
    align: "center",
  },
  grid: {
    borderColor: "#e7e7e7",
    row: {
      colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
      opacity: 0.5,
    },
  },
  xaxis: {
    categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
    title: {
      text: "Month",
    },
  },
  yaxis: {
    title: {
      text: "Temperature",
    },
    min: 5,
    //max: 40
  },
  legend: {
    position: "bottom",
    horizontalAlign: "left",
    floating: true,
    offsetY: 0, // -15,
    offsetX: -0,
  },
});

const setPlotOptions = (type = "line") => {
  if (type == "line") {
      console.log("Line")
      chartOptions.value.stroke.dashArray = dataDash.value
      chartOptions.value.stroke.width = 2
      chartOptions.value.stroke.curve = "straight"
      chartOptions.value.fill.type = "stroke" // "solid"
    } 
    if (type == "bar") {
      console.log("Bar")
      chartOptions.value.stroke.dashArray = 0
      chartOptions.value.fill = {
              type: 'pattern',
              opacity: 1,
              pattern: {
                style: dataPattern.value, // string or array of strings
              },
            }
    }
}

/*
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
*/

watch(currentPresetName, (newValue, oldValue) => {
  console.log("Theme changed:", newValue);
  chartOptions.value.plugins.title.color =
    newValue == "dark" ? "white" : "black";
  updateOptions();
});

watch(
  () => props.type,
  (newValue, oldValue) => {
    console.log("Type changed:", newValue);
    chartType.value = newValue;
    chartOptions.value.chart.type = newValue;
    setPlotOptions(props.type)
    updateOptions();
  }
);

watch(
  () => props.stacked,
  async (newValue, oldValue) => {
    console.log("Stacked changed:", newValue);
    chartOptions.value.chart.stacked = newValue;
    // stacked option is not dynamically changed. use nexttick and loaded flag
    updateOptions();
  }
);

watch(
  () => props.range,
  (newValue, oldValue) => {
    console.log("Range changed:", newValue);
  }
);

watch(
  () => props.dataUrl,
  async (newValue, oldValue) => {
    console.log("Data URL changed:", newValue);
    //if (theChart.value) await theChart.value.clear()
    await loadData();
    // update title as well
    chartOptions.value.plugins.title.text = props.dataName;
    updateOptions();
  }
);

watch(
  () => props.animate,
  (newValue, oldValue) => {
    console.log("Animate changed:", newValue);
  }
);

const updateOptions = async () => {
  if (!theChart.value) return;
  theChart.value.updateOptions(chartOptions.value);
  /*
  dataLoaded.value = false
  await nextTick();
  dataLoaded.value = true
  */
};

const loadData = async () => {
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
      await updateOptions();
    } else {
      // assume csv
      const csvString = await response.text();
      //console.log("raw CSV:",csvString)
      Papa.parse(csvString, {
        header: true,
        dynamicTyping: true,
        complete: async function (results) {
          //console.log("CSV parsed:", results.data);
          data.value = results.data;
          await updateOptions();
        },
      });
    }
    await nextTick();
    dataLoaded.value = true;
  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
};

onMounted(async () => {
  //  initialize colors
  for (let i = 0; i < 8; i++) {
    dataColor.value[i] = getDataSymbol(i%2).color;
    // dataSymbols.value[i] = getDataSymbol(i).symbol
    dataSymbol.value[i] = (i >> 1 ) % 2 ? "square" : "circle";
    dataSymbolSize.value[i] = (i >> 2 ) % 2 ? 10 : 7;
    dataDash.value[i] = 0 // (i >> 2 ) % 2 ? 0 : 5;
    switch (i) {
      case 0:
      case 1:
        dataPattern.value[i] = "circles"
        break
      case 2:
      case 3:
        dataPattern.value[i] = "slantedLines"
        break
      case 4:
      case 5:
        dataPattern.value[i] = "verticalLines"
        break
      default:
        dataPattern.value[i] = "horizontalLines"
        break
    }
  }

  setPlotOptions(props.type)

  if (configStore.getTheme == "dark") {
    console.log("Dark theme detected");
  } else {
    console.log("Light theme detected");
  }

  await loadData();

  try {
    // data might have multiple series
    const seriesCount = data.value.length;
    console.log("Series count:", seriesCount);
  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
});
</script>

<template>
  <div style="position: relative; width: 100%; height: 100%">
    <apexchart
      v-if="dataLoaded"
      :options="chartOptions"
      :series="chartData"
      ref="theChart"
      height="100%"
    ></apexchart>
  </div>
</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
