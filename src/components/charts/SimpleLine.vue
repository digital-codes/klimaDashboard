<script setup>
import { ref, onMounted, watch } from "vue";
import { nextTick } from 'vue';

import VChart, { UPDATE_OPTIONS_KEY } from "vue-echarts";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

// data parser
import Papa from 'papaparse';
// https://www.data-forge-js.com/
// https://github.com/data-forge/data-forge-ts/blob/master/docs/guide.md
import * as dataForge from 'data-forge'

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


const props = defineProps({
  /* Add your props here */
  dataUrl: {
    type: String,
    required: true,
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

watch(() => props.range, (newValue, oldValue) => {
  console.log("Range changed:", newValue);
});

watch(() => props.dataUrl, async (newValue, oldValue) => {
  console.log("Data URL changed:", newValue);
  if (theChart.value) await theChart.value.clear()
  await loadData();

});

watch(() => props.animate, (newValue, oldValue) => {
  console.log("Animate changed:", newValue);
});

const updateOptions = async () => {
  console.log("Updating from data:", data.value);
  // we have to know if we get 1 or 2 series from data.
  // assume we always have an array. 
  // in case the inner data is an array too, we have multiple series
  const df = new dataForge.DataFrame(data.value)
  console.log(df.head(3).toString());
  const cols = df.getColumnNames()
  console.log("Cols:", cols)

  if (df.hasSeries("Datum")) {
    console.log("With Datum")
    datakeys.value = df.getSeries("Datum").toArray()
  } else {
    console.log("No Datum")
  } 
  

  let seriesCount = 1;
  if (Array.isArray(data.value)) {
    // Continue with your code here...
    if (Array.isArray(data.value[0])) {
      seriesCount = data.value.length;
    }
  } else {
    console.error("Data is not an array");
    data.value = [data.value]
  }
  console.log("Series count:", seriesCount);
  // dataframe tests
  let dfArray = []
  if (seriesCount == 1) {
    const df = new dataForge.DataFrame(data.value)
    dfArray.push(df)
    console.log(df.head(5).toString());

    const dt = df.toArray();
    console.log("Data:", dt)
    const cols = df.getColumnNames()
    console.log("Cols:", cols)

  } else {
    for (let i = 0; i < seriesCount; i++) {
      console.log("Processing series:", i)
      const df = new dataForge.DataFrame(data.value[i])
      dfArray.push(df)
      console.log(df.head(5).toString());
    }
  }
  // ready to merge into options ..
  const arrayOfColumnNames = dfArray[0].getColumnNames();
  console.log("Final cols:", arrayOfColumnNames)

  if (arrayOfColumnNames.length < 2) {
    console.error("Need at least 2 columns for charting")
    return
  }
  if (arrayOfColumnNames.length == 2) {
    chartOptions.value.yAxis.name = arrayOfColumnNames[1]
    //chartOptions.value.xAxis.data = dfArray[0].index.map((item, index) => index);
  } else {
    chartOptions.value.yAxis.name = "Value"
  }


  chartOptions.value.xAxis.data = []
  chartOptions.value.xAxis.data = arrayOfColumnNames.map((item) => item);
  chartOptions.value.xAxis.data = arrayOfColumnNames.map((item) => item);
  console.log("X-axis data:", chartOptions.value.xAxis.data)
  chartOptions.value.series = [];
  for (let i = 1; i < seriesCount; i++) {
    chartOptions.value.series.push({
      type: "line",
      name: "Series " + i,
      // data: dfArray[i][arrayOfColumnNames[1]].map((item) => item[datakeys.value[i]]),
      data: dfArray[i][arrayOfColumnNames[1]].map((item) => item[datakeys.value[i]]),
      /*
      type: "line",
      name: datakeys.value[i],
      data: data.value.map((item) => item[datakeys.value[i]]),
      */
      symbol: 'circle',
      symbolSize: 20,
      label: {
        show: true,
        position: 'top',
        color: 'black',
        fontSize: 12,
      },
    });
  }
  console.log("Options updated:", chartOptions.value);
}

const loadData = async () => {
  try {
    console.log("Fetching: ", props.dataUrl);
    const response = await fetch(props.dataUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    datakeys.value = []
    if (props.dataUrl.endsWith(".json")) {
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

const chartOptions = ref({
  //darkMode: "auto",
  tooltip: {
    trigger: 'axis'
  },
  toolbox: {
    show: true,
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      dataView: { readOnly: true },
      magicType: { type: ['line', 'bar', 'stack'] },
      restore: {},
    }
  },
  title: {
    "show": true,
    "left": "center",
    "text": "Line chart example",
    "textStyle": {
      //"color": "#0f0",
      "fontSize": 20
    }
  },
  legend: {
    right: 'auto',
    top: 'bottom',
    show: true,
    type: 'scroll',
  },
  "aria": {
    "enabled": true,
    "description": "Line chart example",
    show: true,
  },
  // backgroundColor: "#333",
  xAxis: {
    name: "X-axis",
    nameLocation: "center",
    nameGap: 30,
    axisLabel: {
      "show": true
      //formatter: '{value} [Unit-X]'
    },
    type: "category",
    //data: dummyData.map((item) => item.date),
  },
  yAxis: {
    name: "Y-axis",
    nameLocation: "center",
    nameGap: 30,
    axisLabel: {
      "show": true
      //formatter: '{value} [Unit-Y]'
    },
    type: "value",
  },
  series: []
}
)

/*
        {
          type: "line",
          name: "Series 1",
          data: dummyData.map((item) => item.value),
          symbol: 'circle',
          symbolSize: 20,
          label: {
            show: true,
            position: 'top',
            color: 'black',
            fontSize: 12,
          },
          // itemstyle for bar chart
          itemStyle:
          {
            decal:
            {
              dashArrayX:5,
              dashArrayY:1,
              rotation: -45,
              color:"#000",
            }
          }
        },
        {
          type: "line",
          name: "Series 2",
          data: dummyData2.map((item) => item.value),
          symbol: 'diamond',
          symbolSize: 20,
          label: {
            show: true,
            position: 'top',
            color: 'black',
            fontSize: 12,
          },
          // itemstyle for bar chart
          itemStyle:
          {
            decal:
            {
              dashArrayX:5,
              dashArrayY:1,
              rotation: 45,
              //symbol: 'diamond',
              //symbolSize:1,
              color:"#000",
            }
          }
        },
      ],

*/
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

    /*
    const lines = data.split("\n");
    const xAxisData = [];
    const seriesData = [];
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].split(",");
      xAxisData.push(line[0]);
      seriesData.push(parseFloat(line[1]));
    }
    chartOptions.value = {
      xAxis: {
        type: "category",
        data: data.xAxisData,
      },
      yAxis: {
        type: "value",
      },
      series: [
        {
          type: "line",
          data: data.seriesData,
        },
      ],
    };
    */
    const dummyData = [
      { date: "2022-01-01", value: 10 },
      { date: "2022-01-02", value: 15 },
      { date: "2022-01-03", value: 8 },
      { date: "2022-01-04", value: 12 },
      { date: "2022-01-05", value: 6 },
    ];

    const dummyData2 = [
      { date: "2022-01-01", value: 20 },
      { date: "2022-01-04", value: 25 },
      { date: "2022-01-05", value: 18 },
      { date: "2022-01-06", value: 22 },
      { date: "2022-01-07", value: 9 },
    ];




  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
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
