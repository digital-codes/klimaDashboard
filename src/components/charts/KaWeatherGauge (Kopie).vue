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



// data parser
import Papa from 'papaparse';
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
  // optional X axis label
  labelX: {
    type: String,
    default: "",
  },
  // optional Y axis label
  labelY: {
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

const theChart1 = ref(null);
const theChart2 = ref(null);
const chartTheme = ref(currentPresetName) // already reactive. don't watch for theme
const dataLoaded = ref(false);
const data = ref(null);
const datakeys = ref(null);

const chartStyle = ref(
  {
    height: '100%',
    width: '50%', 
    display:'inline-flex'
  }
)

watch(currentPresetName, (newValue, oldValue) => {
  console.log("Theme changed:", newValue);
  chartTheme.value = newValue;
  if (newValue == "dark") {
    chartOptions.value.series[0].color = ["white","orange","yellow"]
  } else {
    chartOptions.value.series[0].color = ["black","blue","red"]
  }
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

watch(() => props.dataUrl, async (newValue, oldValue) => {
  //console.log("Data URL changed:", newValue);
  if (theChart1.value) await theChart1.value.clear()
  if (theChart2.value) await theChart2.value.clear()
  await loadData();
  // also update title
  chartOptions.value.title.text = props.dataName

});

watch(() => props.dataName, async (newValue, oldValue) => {
  // update title
  chartOptions.value.title.text = props.dataName

});

watch(() => props.animate, (newValue, oldValue) => {
  console.log("Animate changed:", newValue);
});


const updateOptions = async () => {
  const size = breakpoint.smUp ? "large" : "small";
  console.log("Size:", size)
  chartOptions1.value.series[0].data[0].value = 20 //Math.floor(Math.random() * 50)
  chartOptions1.value.series[0].data[1].value = -10 // Math.floor(Math.random() * 50)
  chartOptions2.value.series[0].data[0].value = 27 // Math.floor(Math.random() * 50)
  chartOptions2.value.series[0].data[1].value = 2 // Math.floor(Math.random() * 50)
  return
  chartOptions.value = await updateEchartsOptions(chartOptions.value, 
    data.value, props.dataX, props.dataClasses, props.dataColumns, props.type, props.stacked, size)
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
      const dt = await response.json();
      console.log("JSON:", dt);
      const dataPoint = dt.albtal.body[0]  // need to get first element
      console.log("Cols:", props.dataColumns)
      let vals = {
        measured_at:[dataPoint.measured_at]
      }
      for (const key in dataPoint.data) {
        if (props.dataColumns.includes(key)) {
          vals[key] = [dataPoint.data[key]]
        }
      }
      data.value = vals
      // current time
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone
      //console.log("TZ:", tz)
      const now = new Date()
      //console.log("Now:", now)
      const mt = new Date(data.value.measured_at[0])
      //console.log("MT:", mt)
      const delta = Math.ceil((now.valueOf() - mt.valueOf()) / (1000 * 60))
      //console.log("Delta (minutes):", delta)
      data.value.delta = [delta]
      console.log("JSON:", data.value);

    } else { // assume csv
      throw new Error("CSV not supported yet")
    }
    //if (theChart.value) await theChart.value.setOption(chartOptions.value, true, true);
    if (theChart1.value) await theChart1.value.clear()
    if (theChart2.value) await theChart2.value.clear()
    await updateOptions()
    await nextTick();
    dataLoaded.value = true;
  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
}

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



const chartOptions1 = ref(
  {
  title : {
    text: props.dataName,
    left: 'center',
    top: 'top'
  },
  series:[
  {
      type: 'gauge',
      name:"sefwef",
      legend: {
        show:true,
        itemGap:20,
      },
      center: ['50%', '80%'],
      radius: '80%',
      startAngle: 180,
      endAngle: 0,
      min: -20,
      max: 50,
      splitNumber: 14,
      color:["#ff0000","#00ff00","#0000ff"],      
      progress: {
        show: true,
        overlap: false,
        roundCap: false,
        width: 20,
        itemStyle: {
          borderWidth: 2,
          borderColor: '#000000'
        }
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
          name:"A",
          title: {
            show:true,
            offsetCenter: ["-50%", 20]            
          },
          value: 20,
        },
        {
          name:"B",
          title: {
            show:true,
            offsetCenter: [0, 20]            
          },
          value: 50
        },
        {
          name:"C",
          title: {
            show:true,
            offsetCenter: ["50%", 20]            
          },
          value: 30
        }
      ]
    }
  ]
}
)

const chartOptions2 = ref(
  {
  title : {
    text: props.dataName + 2,
    left: 'center',
    top: 'top'
  },
  series:[
  {
      type: 'gauge',
      name:"sefwef",
      legend: {
        show:true,
        itemGap:20,
      },
      center: ['50%', '80%'],
      radius: '80%',
      startAngle: 180,
      endAngle: 0,
      min: -20,
      max: 50,
      splitNumber: 14,
      color:["#ff0000","#00ff00","#0000ff"],      
      progress: {
        show: true,
        overlap: false,
        roundCap: false,
        width: 20,
        itemStyle: {
          borderWidth: 2,
          borderColor: '#000000'
        }
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
          name:"A",
          title: {
            show:true,
            text:"ddd",
            offsetCenter: ["-50%", 20]            
          },
          value: 20,
        },
        {
          name:"B",
          title: {
            show:true,
            offsetCenter: [0, 20]            
          },
          value: 50
        },
        {
          name:"C",
          title: {
            show:true,
            offsetCenter: ["50%", 20]            
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
  await nextTick();
  await loadData();

  dataLoaded.value = true;

/*
option = {
    title: {
    show:true,
    text:"Temperatur",
    left:"center"
  },
  series: [
    {
      type: 'gauge',
      name:"sefwef",
      legend: {
        show:true,
        itemGap:20,
      },
      center: ['50%', '60%'],
      startAngle: 180,
      endAngle: 0,
      min: -20,
      max: 50,
      splitNumber: 14,
      color:["#ff0000","#00ff00","#0000ff"],      
      progress: {
        show: true,
        overlap: false,
        roundCap: false,
        width: 20,
        itemStyle: {
          borderWidth: 2,
          borderColor: '#000000'
        }
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
        distance: 0,
        color: '#999',
        fontSize: 30
      },
      anchor: {
        show: false
      },
      title: {
        show: true,
        //offsetCenter : [100, '20%'],
        text:"123"
      },
      detail: {
        show: false,
      },
      data: [
        {
          name:"sdknfn",
          title: {
            show:true,
            text:"ddd",
            offsetCenter: ["-50%", 0]            
          },
          value: 20,
        },
        {
          name:"yxxx",
          title: {
            show:true,
            offsetCenter: [0, 0]            
          },
          value: 50
        },
        {
          name:"1213",
          title: {
            show:true,
            offsetCenter: ["50%", 0]            
          },
          value: 30
        }
      ]
    }
  ]
};
*/



});
</script>

<template>
  <v-chart v-if="dataLoaded" 
  ref="theChart1" 
  :option="chartOptions1" 
  :style="chartStyle"
  :theme="chartTheme"
  :init-options="{ renderer: 'canvas' }"
  autoresize
  >
  </v-chart>
  <v-chart v-if="dataLoaded" 
  ref="theChart2" 
  :style="chartStyle"
  :option="chartOptions2" 
  :theme="chartTheme"
  :init-options="{ renderer: 'canvas' }"
  autoresize
  >
  </v-chart>
</template>

<style scoped>
</style>

