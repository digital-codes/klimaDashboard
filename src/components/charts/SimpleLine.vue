<script setup>
import { ref, onMounted, watch } from "vue";
import { nextTick } from 'vue';

import VChart, { UPDATE_OPTIONS_KEY } from "vue-echarts";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

// data parser
import Papa from 'papaparse';

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
  const keys = Object.keys(data.value[0]);
  console.log(keys)
    chartOptions.value.xAxis.data = []
    chartOptions.value.xAxis.data = data.value.map((item) => item[datakeys.value[0]]);
    chartOptions.value.series = [];
    for (let i = 1; i < datakeys.value.length; i++) {
        chartOptions.value.series.push({
            type: "line",
            name: datakeys.value[i],
            data: data.value.map((item) => item[datakeys.value[i]]),
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
        } else { // assume csv
            const csvString = await response.text();
            Papa.parse(csvString, {
                header: true,
                dynamicTyping: true,
                complete: function (results) {
                    console.log("CSV parsed:", results.data);
                    data.value = results.data;
                }
            });
        }
        for (const key in data.value[0]) {
            datakeys.value.push(key)
        }
        console.log("Data:", data.value);
        console.log("Keys:", datakeys.value);
        // update options
        updateOptions();
        dataLoaded.value = true;
        await nextTick();
        console.log("Data loaded:", data);
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
