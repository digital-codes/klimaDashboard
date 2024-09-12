<script setup>
import { ref, onMounted, watch } from "vue";
import { nextTick } from 'vue';

import VChart, { UPDATE_OPTIONS_KEY } from "vue-echarts";

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

// breakpoint
import { useBreakpoint } from "vuestic-ui";
const breakpoint = useBreakpoint();

// import composables
import { lineBarDefaults, updateEchartsOptions } from '@/composables/EchartsUtils';


// https://www.data-forge-js.com/
// https://github.com/data-forge/data-forge-ts/blob/master/docs/guide.md

import { use } from "echarts/core";
import { SVGRenderer, CanvasRenderer } from "echarts/renderers";
// normally, only a single chart type is needed
// unless toolbox allows to switch types (like here ...)
import { GaugeChart } from "echarts/charts";
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

const props = defineProps({
  /* Add your props here */
  data: {
    type: Object,
    required: true,
  },
  dataName: {
    // localized title
    type: String,
    default: "Weather Data",
  },
  dataColumn: {
    // this value identifies the column for the specs
    type: String,
    default: "temperature",
  },
  // data labels
  dataLabels: {
    type: Array,
    required: true
  }
});

use([
  CanvasRenderer,
  SVGRenderer,
  GaugeChart,
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent
]);



const theChart = ref(null);
const chartTheme = ref(currentPresetName) 
const dataLoaded = ref(false);
const data = ref(null);
const datakeys = ref(null);
const dataRange = ref([0, 100]);

const chartStyle = ref(
  {
    height: '100%',
    width: '100%',
    //display:'inline-flex'
  }
)


const setTheme = (theme) => {
  chartTheme.value = theme;
  if (theme == "dark") {
    chartOptions.value.series[0].color = ["white","orange","yellow","cyan"]
  } else {
    chartOptions.value.series[0].color = ["green","blue","red","orange"]
  }
}

watch(currentPresetName, (newValue, oldValue) => {
  console.log("Theme changed:", newValue);
  setTheme(newValue)
});

watch(() => props.type, (newValue, oldValue) => {
  //console.log("Type changed:", newValue);
  updateOptions()
});

watch(() => props.stacked, (newValue, oldValue) => {
  //console.log("Stacked changed:", newValue);
  updateOptions()
});


watch(() => props.range, (newValue, oldValue) => {
  console.log("Range changed:", newValue);
});

// monitor data changes
watch(() => props.data, async (newValue, oldValue) => {
  //console.log("Data changed:", newValue);
  // also update title
  chartOptions.value.title.text = props.dataName
  await updateOptions();

});

watch(() => props.dataName, async (newValue, oldValue) => {
  // update title
  chartOptions.value.title.text = props.dataName

});



const updateOptions = async () => {
  const size = breakpoint.smUp ? "large" : "small";
  //console.log("name:", props.dataName)
  //console.log("col:", props.dataColumn)

  for (const i in props.dataLabels) {
    chartOptions.value.series[0].data[i].value = props.data.values[i] * columnSpecs(props.dataColumn).scale
    chartOptions.value.series[0].data[i].name = props.dataLabels[i]
  }

  dataLoaded.value = true;

}


const columnSpecs = (name) => {
  let specs = {}
  switch (name) {
    case "temperature":
      specs = {
        unit: "°C",
        min: -20,
        max: 50,
        split: 14,
        scale: 1
      }
      break
    case "humidity":
      specs = {
        unit: "%",
        min: -0,
        max: 100,
        split: 10,
        scale: 1
      }
      break
      case "irradiation":
      specs = {
        unit: "W/m²",
        min: 0,
        max: 1000,
        split: 10,
        scale: 1
      }
      break
      case "rain":
      specs = {
        unit: "l/h",
        min: 0,
        max: 500,
        split: 10,
        scale: (.2*6)
      }
      break
      case "pressure":
      specs = {
        unit: "mbar",
        min: 900,
        max: 1100,
        split: 10,
        scale: .01
      }
      break
            
    default:
      alert("Unknown column name: " + name)
      break
  }
  return specs
}

const chartOptions = ref(
  {
    title: {
      text: props.dataName + " [" + columnSpecs(props.dataColumn).unit + "]",
      left: 'center',
      top: 'top'
    },
    tooltip: {
      // specific settings in series
      trigger: "item"
    },
    series: [
      {
        type: 'gauge',
        name: props.dataName,
        legend: {
          show: true,
          itemGap: 20,
        },
        center: ['50%', '80%'],
        radius: '65%',
        startAngle: 180,
        endAngle: 0,
        min: columnSpecs(props.dataColumn).min,
        max: columnSpecs(props.dataColumn).max,
        splitNumber: columnSpecs(props.dataColumn).split,
        colorBy: "data",
        progress: {
          show: true,
          overlap: false,
          roundCap: false,
          width: 20,
          itemStyle: {
            borderWidth: 2,
            borderColor: '#000000',
          }
        },
        tooltip: {
          trigger: "item",
          // formatter: '{b0}: {c0} MT {mt0}',
          valueFormatter: (value) => {
            const v = String(value.toFixed(2)).replace('.', ',') + columnSpecs(props.dataColumn).unit
            return v
          },
          position: ['50%', '50%'],
          // backgroundColor: "#000000",
        },

        pointer: {
          show: false
        },
        axisLine: {
          lineStyle: {
            width: 60
          }
        },
        axisTick: {
          distance: -75,
          splitNumber: 5,
          lineStyle: {
            width: 2,
            color: '#999'
          }
        },
        splitLine: {
          distance: -80,
          length: 14,
          lineStyle: {
            width: 3,
            color: '#999'
          }
        },
        axisLabel: {
          distance: 10,
          color: '#999',
          fontSize: 16
        },
        anchor: {
          show: false
        },
        detail: {
          show: false,
        },
        data: [
          {
            name: "A",
            title: {
              show: true,
              offsetCenter: ["-100%", 20]
            },
            value: 20,
          },
          {
            name: "B",
            title: {
              show: true,
              offsetCenter: ["-100%", 40]
              //offsetCenter: [0, 20]
            },
            value: 50.123
          },
          {
            name: "C",
            title: {
              show: true,
              offsetCenter: ["100%", 20]
            },
            value: 30
          },
          {
            name: "D",
            title: {
              show: true,
              offsetCenter: ["100%", 40]
            },
            value: 30
          }
        ]
      }
    ]
  }
)



onMounted(async () => {

  if (configStore.getTheme == "dark") {
    console.log("Dark theme detected")
  } else {
    console.log("Light theme detected")
  }
  setTheme(configStore.getTheme)
  await nextTick();
  await updateOptions();

  dataLoaded.value = true;


});
</script>

<template>
  <v-chart v-if="dataLoaded" ref="theChart" :option="chartOptions" :style="chartStyle" :theme="chartTheme"
    :init-options="{ renderer: 'canvas' }" autoresize />
</template>

<style scoped></style>
