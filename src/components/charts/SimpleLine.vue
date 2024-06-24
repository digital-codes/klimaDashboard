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
  chartDataUri: {
    type: String,
    required: true,
  },
});

const theChart = ref(null);
const chartTheme = ref(currentPresetName) // already reactive. don't watch for theme

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

  //chartTheme.value = currentPresetName

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
          magicType: { type: ['line', 'bar', 'stack'] },
          restore: {},
          saveAsImage: {
            show: true,
            title: 'Save As Image',
          },
          /*
          myCustBut2: {
            title: 'test option 2',
            icon: 'path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891',
            onclick: async () => {
              alert('Test 2');
              const png = await theChart.value.getDataURL({
                  pixelRatio: 2,
                  backgroundColor: '#fff'
              });
              console.log(png)
            },
          }
        */
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
              /*
              symbol: 'circle',
              symbolSize:1,
              */
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
    };


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
