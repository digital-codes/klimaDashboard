<script setup>
import { ref, onMounted, watch } from "vue";
import { nextTick } from 'vue';

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

// import composables
import getDataSymbol from '@/composables/DataSymbol';


// data parser
import Papa from 'papaparse';
// https://www.data-forge-js.com/
// https://github.com/data-forge/data-forge-ts/blob/master/docs/guide.md
import * as dataForge from 'data-forge'

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
const chartType = ref("line")


const chartData = ref(
  [
    {
      name: "High - 2013",
      data: [28, 29, 33, 36, 32, 32, 33]
    },
    {
      name: "Low - 2013",
      data: [12, 11, 14, 18, 17, 13, 13]
    }
  ]
)


const chartOptions = ref({
  // apexcharts
  chart: {
    //height: 350,
    height:100,
    //width:"100%",
    type: 'line',
    dropShadow: {
      enabled: true,
      color: '#000',
      top: 18,
      left: 7,
      blur: 10,
      opacity: 0.2
    },
    zoom: {
      enabled: false
    },
    toolbar: {
      show: false
    }
  },
  colors: ['#77B6EA', '#545454'],
  dataLabels: {
    enabled: true,
  },
  stroke: {
    curve: 'smooth'
  },
  title: {
    text: 'Average High & Low Temperature',
    align: 'left'
  },
  grid: {
    borderColor: '#e7e7e7',
    row: {
      colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
      opacity: 0.5
    },
  },
  markers: {
    size: 1
  },
  xaxis: {
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    title: {
      text: 'Month'
    }
  },
  yaxis: {
    title: {
      text: 'Temperature'
    },
    min: 5,
    max: 40
  },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    floating: true,
    offsetY: -25,
    offsetX: -5
  }
}
)

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
  chartOptions.value.plugins.title.color = newValue == "dark" ? "white" : "black"
  updateOptions()
});

watch(() => props.type, (newValue, oldValue) => {
  console.log("Type changed:", newValue);
  chartType.value = newValue
  updateOptions()
});

watch(() => props.stacked, async (newValue, oldValue) => {
  console.log("Stacked changed:", newValue);
  chartOptions.value.scales.x.stacked = newValue
  chartOptions.value.scales.y.stacked = newValue
  // stacked option is not dynamically changed. use nexttick and loaded flag
  updateOptions()

});


watch(() => props.range, (newValue, oldValue) => {
  console.log("Range changed:", newValue);
});

watch(() => props.dataUrl, async (newValue, oldValue) => {
  console.log("Data URL changed:", newValue);
  //if (theChart.value) await theChart.value.clear()
  await loadData();
  // update title as well
  chartOptions.value.plugins.title.text = props.dataName
  updateOptions()
});

watch(() => props.animate, (newValue, oldValue) => {
  console.log("Animate changed:", newValue);
});


const updateOptions = async () => {
  console.log("Updating options disabled")
  return
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


onMounted(async () => {

  if (configStore.getTheme == "dark") {
    console.log("Dark theme detected")
  } else {
    console.log("Light theme detected")
  }

  await loadData();

  try {
    // data might have multiple series
    const seriesCount = data.value.length
    console.log("Series count:", seriesCount)


  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
});
</script>

<template>
  <!-- 
  <apexchart v-if="dataLoaded" width="500" type="line" :options="chartOptions" :series="chartData"></apexchart>

  -->  
  <apexchart v-if="dataLoaded" :options="chartOptions" :series="chartData" height="200"></apexchart>

</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
