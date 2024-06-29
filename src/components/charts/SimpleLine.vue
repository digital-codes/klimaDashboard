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

});

watch(() => props.animate, (newValue, oldValue) => {
  console.log("Animate changed:", newValue);
});

const parseData = (data) => {
  if (typeof data === 'number') {
    return data;
  } else {
    return parseFloat(data.replace(",", "."));
  }
}

const dataSymbol = (index) => {
  let sym
  const isDark = configStore.getTheme == "dark"
  const col = index % 2 ? (isDark? 'rgb(31,51,153)' : 'rgb(41,68,205)') : (isDark ? 'rgb(228,193,23)' : 'rgb(177,150,18)')
  let pattern
  // pattern is for bar charts, symbols is for line charts, basically
  // The overall rotation angle (in radians) of the pattern
  switch (index) {
    case 0:
    case 1:
      sym = 'circle'
      pattern = Math.PI / 4
      break;
    case 2:
    case 3:
      sym = 'diamond'
      pattern = -Math.PI / 4
      break;
      case 4:
    case 5:
      sym = 'triangle'
      pattern = Math.PI / 8
      break;
    case 6:
    case 7:
      sym = 'rectangle'
      pattern = -Math.PI / 8
      break;
    default: 
    console.error("Unknown index:",index)
      break;
  }
  return {symbol:sym,color:col, pattern:pattern}   
}

const updateOptions = async () => {
  console.log("Updating from data:", data.value);
  // we have to know if we get 1 or 2 series from data.
  // assume we always have an array. 
  // in case the inner data is an array too, we have multiple series
  const df = new dataForge.DataFrame(data.value)
  console.log(df.head(3).toString());
  const cols = df.getColumnNames()
  //console.log("Cols:", cols)

  // input differs by identifiers for category (X-axis), value (Y-Axis), group
  // and selected group names
  let seriesData

  if (props.dataX == "") {  // no X-axis given 
    console.log("No X-Axis")
    return
  }
  console.log("X-Axis:", props.dataX)

  const chartData = df.toArray();
  let categories = chartData.map(item => item[props.dataX]).filter((value, index, self) => self.indexOf(value) === index);
  categories = categories.filter(category => category !== null);
  //console.log("Categories:", categories, categories.length)

  let classes = []
  // filter classes
  if (props.dataClasses && Array.isArray(props.dataClasses) && props.dataClasses.length > 0) {
    const classId = props.dataClasses[0]
    //console.log("Filtering by classes on:", classId)
    if (props.dataClasses.length > 1) {
      classes = props.dataClasses.slice(1)
    } else {
      classes = df.getSeries(classId).distinct().toArray()
    }
    //console.log("Filtering classes:", classes)
    seriesData = chartData.filter(item => classes.includes(item[classId]));

  } else {
    seriesData = chartData;
  }

  // console.log("Filtered classes:", seriesData)

  let columns = []
  if (props.dataColumns && Array.isArray(props.dataColumns) && props.dataColumns.length > 0) {
    columns = props.dataColumns
  } else {
    //console.log("No columns given")
    columns = df.getColumnNames()
  }
  //console.log("Initial  columns:", columns)

  // don't exclude class name from columns here
  const excludeCols = [props.dataX]
  // console.log(" Excluding columns:", excludeCols)
  // instead, include the class column here
  const includedColumns = columns.filter(column => !(excludeCols.includes(column)))
  if (props.dataClasses && Array.isArray(props.dataClasses) && props.dataClasses.length > 0) {
    includedColumns.push(props.dataClasses[0])
  }  
  // console.log("Included columns:", includedColumns)

  // series created from either classes or columns
  // if length of classes > 1 we have multiple series and length or columns must be 1
  // if length of columns > 1 we have multiple series and length or classes must be 1
  if (classes.length > 1) {
    console.log("Creating series from classes")
    // create names from classes
    seriesData = classes.map((name, index) => {
      //console.log("Name:",name,", Index:",index)
      const filteredData = chartData.filter(item => item[props.dataClasses[0]] === name);
      //console.log("Filtered Data:", filteredData)
      return {
        name: name,
        //data: filteredData.map(item => parseData(item[props.dataColumns[0]])),
        data: categories.map(position => {
          //console.log("Position:",position)
          if (filteredData.find(item => item[props.dataX] === position) == null) {
            return null
          } else {
            return parseData(filteredData.find(item => item[props.dataX] === position)[props.dataColumns[0]])
          }
        }),
        type: props.type,
        stack:props.stacked ? 'stack' : null,
        symbol: dataSymbol(index).symbol,
        color: dataSymbol(index).color,
        symbolSize: 16,
        label: {
          show: false,
          position: 'top',
          color: 'black',
          fontSize: 12,
        },
        itemStyle:
          {
            decal:
            {
              dashArrayX:5,
              dashArrayY:1,
              rotation: dataSymbol(index).pattern,
              color:"#000",
            }
          }
      };
    });
  } else {
    // create names from columns
    console.log("Creating series from columns")
    // if we have classes, remove the corresponding column from included columns
    const valueColumns = classes.length > 0 ? includedColumns.filter(item => item != props.dataClasses[0]) : includedColumns
    seriesData = valueColumns.map((column,index) => {
      //console.log("Column:",column)
      return {
        name: column,
        data: categories.map(position => {
          //console.log("Position:",position)
          const item = chartData.find(item => item[props.dataX] === position)
          if (item == null) {
            //console.log("No data for position:",position)
            return null
          } else {
            //console.log("Data at position:",position,item)
            return parseData(chartData.find(item => item[props.dataX] === position)[column])
          }
        }),
        type: props.type,
        stack:props.stacked ? 'stack' : null,
        symbol: dataSymbol(index).symbol,
        color: dataSymbol(index).color,
        symbolSize: 16,
        label: {
          show: false,
          position: 'top',
          color: 'black',
          fontSize: 12,
        },
        itemStyle:
          {
            decal:
            {
              dashArrayX:5,
              dashArrayY:1,
              rotation: dataSymbol(index).pattern,
              color:"#000",
            }
          }
      };
    });
  }

  // console.log("Final Series:", seriesData)

  chartOptions.value.xAxis.type = "category"
  chartOptions.value.xAxis.data = categories
  chartOptions.value.yAxis = { type: 'value' }
  chartOptions.value.series = seriesData
  //console.log("Options updated:", chartOptions.value);
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
    trigger: 'axis',
    valueFormatter: (value) => value != null ? value.toFixed(1) : "N/A",
  },
  toolbox: {
    show: true,
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      //dataView: { readOnly: true },
      //magicType: { type: ['line', 'bar', 'stack'] },
      //restore: {},
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
