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

import { Bar, Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, LineController, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale, LineController, PointElement)


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

const chartData = ref({
  labels: ['January', 'February', 'March'],
  datasets: [
    {
      label: 'Data One',
      backgroundColor: '#f87979',
      data: [40, 20, 12]
    },
    {
      label: 'Data Two',
      backgroundColor: '#4849f9',
      data: [45, 10, 32]
    }
  ]
}
)


watch(currentPresetName, (newValue, oldValue) => {
  console.log("Theme changed:", newValue);
  chartTheme.value = newValue;
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
  dataLoaded.value = false
  await nextTick();
  dataLoaded.value = true
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


const updateOptions = async () => {
  console.log("Updating options disabled")
  return
  console.log("Updating from data:", data.value);
  // we have to know if we get 1 or 2 series from data.
  // assume we always have an array. 
  // in case the inner data is an array too, we have multiple series
  let df = new dataForge.DataFrame(data.value)
  //console.log(df.toString())
  //console.log("Dataframe:", df.head(3).toString());
  let cols = df.getColumnNames()
  console.log("Cols:", cols)

  if (cols.length == 0) {
    console.log("No columns");
    cols = Object.keys(data.value)
    console.log("Keys:", cols);
    if (cols.length == 0) {
      console.log("Again no columns")
      return
    }
    const tabularData = [];
    for (const key of cols) {
      const items = data.value[key];
      for (const item of items) {
        item.key = key;
        tabularData.push(item);
      }
    }

    df = new dataForge.DataFrame(tabularData);
    // df = new dataForge.DataFrame(data.value[keys[0]])
    // console.log("Dataframe:", df.toString());
  }

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
        stack: props.stacked ? 'stack' : null,
        symbol: getDataSymbol(index).symbol,
        color: getDataSymbol(index).color,
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
            dashArrayX: 5,
            dashArrayY: 1,
            rotation: getDataSymbol(index).pattern,
            color: "#000",
          }
        }
      };
    });
  } else {
    // create names from columns
    console.log("Creating series from columns")
    // if we have classes, remove the corresponding column from included columns
    const valueColumns = classes.length > 0 ? includedColumns.filter(item => item != props.dataClasses[0]) : includedColumns
    seriesData = valueColumns.map((column, index) => {
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
        stack: props.stacked ? 'stack' : null,
        symbol: getDataSymbol(index).symbol,
        color: getDataSymbol(index).color,
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
            dashArrayX: 5,
            dashArrayY: 1,
            rotation: getDataSymbol(index).pattern,
            color: "#000",
          }
        }
      };
    });
  }

  // console.log("Final Series:", seriesData)

  chartOptions.value.xAxis.type = "category"
  chartOptions.value.xAxis.data = categories
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


const chartOptions = ref({
  // chartjs
  type: 'line',
  responsive: true, // requires parent div position relative
  maintainAspectRatio: false,
  scales: {
    x: {
      stacked: false
    },
    y: {
      stacked: false
    }
  },
}
)

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
    <Bar v-if="dataLoaded" ref="theChart" 
    :style="chartStyle"
    :data="chartData"
    :options="chartOptions"
    />

  -->
  <div style="position: relative; width: 100%; height: 100%;">
    
    <Line v-if="dataLoaded && (chartType == 'line')" ref="theChart" :style="chartStyle" :data="chartData"
      :options="chartOptions" />
    <Bar v-if="dataLoaded && (chartType == 'bar')" ref="theChart" :style="chartStyle" :data="chartData"
      :options="chartOptions" />
    </div>

</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
