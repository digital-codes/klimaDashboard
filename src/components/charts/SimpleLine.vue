<script setup>
import { ref, onMounted, watch, onUnmounted } from "vue";
import { nextTick } from "vue";

import VChart, { UPDATE_OPTIONS_KEY } from "vue-echarts";

import { useConfigStore } from "@/services/configStore";
const configStore = useConfigStore();

// breakpoint
import { useBreakpoint } from "vuestic-ui";
const breakpoint = useBreakpoint();

// import composables
import {
  lineBarDefaults,
  updateEchartsOptions,
  setType, setStacked,
} from "@/composables/EchartsUtils";

// data parser
import Papa from "papaparse";
// https://www.data-forge-js.com/
// https://github.com/data-forge/data-forge-ts/blob/master/docs/guide.md

import { use } from "echarts/core";
import { SVGRenderer, CanvasRenderer } from "echarts/renderers";
// normally, only a single chart type is needed
// unless toolbox allows to switch types (like here ...)
import { LineChart, BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";

// optimize later
// import "echarts"

import { useColors } from "vuestic-ui";
const { currentPresetName } = useColors();

const emit = defineEmits(["xrange", "yrange"]);

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
  ariaLabel: {
    type: String,
    default: "Aria LineChart",
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
    default: 0,
  },
  // optional range.
  rangeValue: {
    type: Number,
    default: 0,
  },
  // optional range axis.
  rangeAxis: {
    type: String,
    default: "",
  },
  type: {
    type: String,
    default: "line",
  },
  locale: {
    type: String,
    default: "de",
  },
  stacked: {
    type: Boolean,
    default: false,
  },
  range: {
    type: Number,
    default: 50,
  },
  animate: {
    type: Boolean,
    default: false,
  },
});

const theChart = ref(null);
const chartTheme = ref(currentPresetName); // already reactive. don't watch for theme
const dataLoaded = ref(false);
const data = ref(null);
const datakeys = ref(null);
const ariaLabel = ref(props.ariaLabel);

const animTimer = ref(null);
const fullXRange = ref({});
const fullData = ref([]);

watch(currentPresetName, (newValue, oldValue) => {
  console.log("Theme changed:", newValue);
  chartTheme.value = newValue;
  if (newValue == "dark") {
    for (let i = 0; i < chartOptions.value.series.length; i++) {
      chartOptions.value.series[i].label.color = "white";
    }
  } else {
    for (let i = 0; i < chartOptions.value.series.length; i++) {
      chartOptions.value.series[i].label.color = "black";
    }
  }
});

watch(
  () => props.rangeValue,
  (newValue, oldValue) => {
    console.log("Range changed:", newValue, props.rangeAxis);
    switch (props.rangeAxis) {
      case "x":
        console.log("Xrange:", newValue);
        const idx = fullXRange.value.range.indexOf(newValue);
        console.log("Index:", idx);
        setupXRange()
        animationDataSlice(idx);
      break;
      case "y":
        chartOptions.value.yAxis.max = props.stacked ? null : newValue;
        break;
      default:
        console.log("No range");
        restoreDataRange()
    }
    // updateOptions();
  }
);

watch(
  () => props.locale,
  (newValue, oldValue) => {
    //console.log("Type changed:", newValue);
    updateOptions();
  }
);

watch(
  () => props.type,
  (newValue, oldValue) => {
    //console.log("Type changed:", newValue);
    // chartOptions.value.type = newValue
    setType(newValue,chartOptions.value)
  }
);

watch(
  () => props.ariaLabel,
  (newValue, oldValue) => {
    //console.log("Type changed:", newValue);
    ariaLabel.value = props.ariaLabel;
  }
);

watch(
  () => props.stacked,
  (newValue, oldValue) => {
    //console.log("Stacked changed:", newValue);
    if (newValue) {
      chartOptions.value.yAxis.max = null;
    } else {
      if ("y" == props.rangeAxis) {
        chartOptions.value.yAxis.max = props.rangeValue;
      }
    }
    setStacked(newValue, chartOptions.value);
    // updateOptions();
  }
);


watch(
  () => props.dataName,
  async (newValue, oldValue) => {
    // update title
    chartOptions.value.title.text = props.dataName;
  }
);

watch(
  () => props.animate,
  (newValue, oldValue) => {
    console.log("Animate changed:", newValue);
    if (newValue) {
      //console.log("X", chartOptions.value.xAxis);
      //console.log("series", chartOptions.value.series);
      // saveData() we save after loading
      startAnimation();
    } else {
      console.log("Anim off");
      if (animTimer.value) {
        clearInterval(animTimer.value);
        restoreDataRange();
        updateOptions();
      }
    }
  }
);

const getDataRange = () => {
  // animation range
  const mxData = [];
  const mnData = [];
  for (const series of chartOptions.value.series) {
    const mx = Math.max(...series.data);
    mxData.push(mx);
    const mn = Math.min(...series.data);
    mnData.push(mn);
  }
  /*
  let mx;
  mx = props.stacked
    ? mxData.reduce((acc, cur) => acc + cur, 0)
    : Math.max(...mxData);

  if (mx > 100) mx = Math.ceil(1.05 * mx);
  else mx += 2;
  */
  const range = { min: Math.min(...mnData), max: Math.max(...mxData), smax: mxData.reduce((acc, cur) => acc + cur, 0) }
  console.log("Range:", range);
  return range
};

const saveData = () => {
  // save data 
  fullData.value = JSON.parse(JSON.stringify(chartOptions.value.series));
  // max data values
  const range = getDataRange();
  // and X range
  fullXRange.value = {
    idx: 0,
    len: chartOptions.value.xAxis.data.length,
    range: JSON.parse(JSON.stringify(chartOptions.value.xAxis.data)),
    max: range.max,
    smax: range.smax
  };
  console.log("Range value max:", fullXRange.value.max);
}

const setupXRange = () => {
  let mx = props.stacked ? fullXRange.value.smax : fullXRange.value.max;
  if (mx > 100) mx = Math.ceil(1.05 * mx);
  else mx += 2;
  chartOptions.value.yAxis.max = mx
};


const startAnimation = () => {
  setupXRange()
  fullXRange.value.idx = 0;
  animationDataSlice(fullXRange.value.idx);
  animTimer.value = setInterval(() => doAnimation(), 1500);
};

const restoreDataRange = () => {
  chartOptions.value.series = fullData.value;
  chartOptions.value.yAxis.max = null;
  updateOptions();
};

const animationDataSlice = (idx) => {
  console.log("Slicing for:", idx);
  for (let i = 0; i < fullData.value.length; i++) {
    //console.log("Animdata",i, fullData.value[i]);
    const dt = fullData.value[i].data;
    //console.log("Series:", dt);
    chartOptions.value.series[i].data = [dt[idx]];
  }
  chartOptions.value.xAxis.data = [fullXRange.value.range[idx]];
  //console.log("Slice:", chartOptions.value.xAxis.data, chartOptions.value.series);
};

const doAnimation = () => {
  if (fullXRange.value.idx < fullXRange.value.len - 1) {
    //console.log("Animate:", fullXRange.value.idx);
    //chartOptions.value.xAxis.data = [fullXRange.value.start, fullXRange.value.end];
    fullXRange.value.idx += 1;
  } else {
    fullXRange.value.idx = 0;
  }
  //console.log("Animate:", fullXRange.value.range[fullXRange.value.idx]);
  animationDataSlice(fullXRange.value.idx);
};

const updateOptions = async () => {
  const size = breakpoint.smUp ? "large" : "small";
  console.log("Size:", size);
  chartOptions.value = await updateEchartsOptions(
    chartOptions.value,
    data.value,
    props.dataX,
    props.dataClasses,
    props.dataColumns,
    props.type,
    props.stacked,
    size,
    props.locale
  );
};

const loadData = async () => {
  try {
    console.log("Fetching: ", props.dataUrl);
    const response = await fetch(props.dataUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    datakeys.value = [];
    if (props.dataFormat == "json") {
      data.value = await response.json();
      //console.log("JSON:", data.value);
    } else {
      // assume csv
      const csvString = await response.text();
      //console.log("raw CSV:",csvString)
      Papa.parse(csvString, {
        header: true,
        dynamicTyping: true,
        complete: async function (results) {
          //console.log("CSV parsed:", results.data);
          data.value = results.data;
        },
      });
    }
    //if (theChart.value) await theChart.value.setOption(chartOptions.value, true, true);
    if (theChart.value) await theChart.value.clear();
    await updateOptions();
    await nextTick();

    // save data from xrange and animation
    saveData()
    // emit limits
    const yrange = getDataRange();
    console.log("Emitting y range",yrange);
    emit("yrange", [yrange.min, yrange.max]);
    const xrange = chartOptions.value.xAxis.data
    console.log("Emitting x range",xrange);
    emit("xrange", [xrange[0], xrange[xrange.length - 1]])

    dataLoaded.value = true;
  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
};

use([
  CanvasRenderer,
  SVGRenderer,
  LineChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
]);

const chartOptions = ref(
  lineBarDefaults(
    props.dataName,
    props.labelX,
    props.labelY,
    breakpoint.smUp ? "large" : "small",
    props.locale
  )
);

onMounted(async () => {
  if (configStore.getTheme == "dark") {
    console.log("Dark theme detected");
  } else {
    console.log("Light theme detected");
  }

  await loadData();
});

onUnmounted(() => {
  if (animTimer.value) {
    clearInterval(animTimer.value);
  }
});
</script>

<template>
  <v-chart v-if="dataLoaded" ref="theChart" :option="chartOptions" :style="{ height: '100%' }" :theme="chartTheme"
    :init-options="{ renderer: 'canvas' }" autoresize :aria-label="ariaLabel">
  </v-chart>
</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
