<script setup>
import { ref, onMounted } from "vue";
import VChart from "vue-echarts";

import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from "echarts/components";

// optimize later
//import "echarts"

const props = defineProps({
  /* Add your props here */
  chartDataUri: {
    type: String,
    required: true,
  },
});

const chartOptions = ref({});

const dataLoaded = ref(false);

onMounted(async () => {
  use([
    CanvasRenderer,
    LineChart,
    TitleComponent,
    TooltipComponent,
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

    chartOptions.value = {
        darkMode: "auto",
        "title": {
            "show": true,
            "left": "center",
            "text": "Line chart example",
            "textStyle": {
                "color": "#ff0",
                "fontSize": 20
            }
        },
        "aria": {
            "enabled":true,
            "description": "Line chart example",
        },
        backgroundColor: "#333",
        xAxis: {
            name: "X-axis",
            nameLocation: "center",
            nameGap: 30,
            axisLabel: {
            "show": true,
            "color": "#f00",
            },
            type: "category",
            data: dummyData.map((item) => item.date),
        },
        yAxis: {
            name: "Y-axis",
            nameLocation: "center",
            nameGap: 30,
            axisLabel: {
            "show": true,
            "color": "#0f0",
            },
            type: "value",
        },
        series: [
            {
                type: "line",
                data: dummyData.map((item) => item.value),
            },
        ],
    };


  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
});
</script>

<template>
  <div class="chart-template">
    <v-chart
      v-if="dataLoaded"
      :option="chartOptions"
      :style="{ height: '400px' }"
    ></v-chart>
  </div>
</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
