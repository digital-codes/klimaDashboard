<script setup>
import { ref, onMounted, watch } from "vue";
import VChart from "vue-echarts";

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
  chartTheme.value = newValue == "dark" ? "dark" : ""
});


const props = defineProps({
  /* Add your props here */
  chartDataUri: {
    type: String,
    required: true,
  },
});

const chartTheme = ref("")

const chartOptions = ref({});

const dataLoaded = ref(false);

onMounted(async () => {
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

  try {
    console.log("Fetching: ", props.chartDataUri);
    const response = await fetch(props.chartDataUri);
    const data = await response.text();
    dataLoaded.value = true;
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


    chartOptions.value = {
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
          magicType: { type: ['line', 'bar','stack'] },
          restore: {},
          saveAsImage: {
            show: true,
            title: 'Save As Image'
          }
        }
      },
      "title": {
        "show": true,
        "left": "center",
        "text": "Line chart example",
        "textStyle": {
          //"color": "#0f0",
          "fontSize": 20
        }
      },
      "aria": {
        "enabled": true,
        "description": "Line chart example",
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
        data: dummyData.map((item) => item.date),
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
      series: [
      {
          type: "line",
          data: dummyData.map((item) => item.value),
        },
        {
          type: "line",
          data: dummyData2.map((item) => item.value),
        },
      ],
    };


  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
});
</script>

<template>
  <v-chart v-if="dataLoaded" :option="chartOptions" :style="{ height: '100%' }" :theme="chartTheme"
    autoresize></v-chart>
</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
