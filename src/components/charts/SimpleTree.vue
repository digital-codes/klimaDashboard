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
  updateEchartsOptions,
  setType,
  setStacked,
} from "@/composables/EchartsUtils";


import { use } from "echarts/core";
import { SVGRenderer, CanvasRenderer } from "echarts/renderers";
// normally, only a single chart type is needed
// unless toolbox allows to switch types (like here ...)
import { TreemapChart } from "echarts/charts";
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

const emit = defineEmits(["xrange", "yrange", "series"]);

const props = defineProps({
  /* Add your props here */
  dataUrl: {
    type: String,
    required: true,
  },
  dataName: {
    type: String,
    default: "TreeChart",
  },
  ariaLabel: {
    type: String,
    default: "Aria TreeChart",
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
  // optional format
  dataDelimiter: {
    type: String,
    default: ";",
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
        setupXRange();
        animationDataSlice(idx);
        break;
      case "y":
        chartOptions.value.yAxis.max = props.stacked ? null : newValue;
        break;
      default:
        console.log("No range");
        restoreDataRange();
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
    setType(newValue, chartOptions.value);
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
  const range = {
    min: Math.min(...mnData),
    max: Math.max(...mxData),
    smax: mxData.reduce((acc, cur) => acc + cur, 0),
  };
  console.log("Range:", range);
  return range;
};

const saveData = () => {
  // save data
  fullData.value = JSON.parse(JSON.stringify(chartOptions.value.series));
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
  data.value = chartData.value;
  dataLoaded.value = true
  await nextTick();
  // emit data after data loaded, else chart intance is not ready
  emit(
    "series",
    {
      chart: theChart.value,
      content: data.value,
    },
    theChart.value
  );

    return
  try {
    console.log("Fetching: ", props.dataUrl);
    const response = await fetch(props.dataUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    datakeys.value = [];
    data.value = await response.json();
    //console.log("JSON:", data.value);
    //if (theChart.value) await theChart.value.setOption(chartOptions.value, true, true);
    if (theChart.value) await theChart.value.clear();
    await updateOptions();
    await nextTick();

    // save data from xrange and animation
    saveData();
    // emit limits
    const yrange = getDataRange();
    console.log("Emitting y range", yrange);
    emit("yrange", [yrange.min, yrange.max]);
    dataLoaded.value = true;
    await nextTick();
    // emit data after data loaded, else chart intance is not ready
    emit(
      "series",
      {
        x: chartOptions.value.xAxis.data,
        cols: fullData.value,
        chart: theChart.value,
      },
      theChart.value
    );
  } catch (error) {
    console.error("Failed to load chart data:", error);
  }
};

use([
  CanvasRenderer,
  SVGRenderer,
  TreemapChart,
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
]);

/*
const chartOptions = ref(
  lineBarDefaults(
    props.dataName,
    props.labelX,
    props.labelY,
    breakpoint.smUp ? "large" : "small",
    props.locale
  )
);
*/

const chartData = ref([
  {
    name: "nodeA",
    upperLabel: {
      show: true,
      color: "#fff",
      height: 30,
    },
    children: [
      {
        name: "nodeAa",
        value: 4,
      },
      {
        name: "nodeAb",
        value: 7,
      },
    ],
  },
  {
    name: "nodeB",
    upperLabel: {
      show: true,
      color: "#fff",
      height: 30,
    },
    children: [
      {
        name: "nodeBa",
        children: [
          {
            name: "nodeBa1",
            value: 8,
          },
          {
            upperLabel: {
              show: true,
              color: "#fff",
              height: 30,
            },
            name: "nodeBa2",
            children: [
              {
                name: "nodeBa2a1",
                value: 3,
              },
              {
                name: "nodeBa2a2",
                value: 1,
              },
            ],
          },
          {
            name: "nodeBa3",
            value: 4,
          },
        ],
      },
    ],
  },
  {
    name: "nodeC",
    upperLabel: {
      show: true,
      color: "#fff",
      height: 30,
    },
    children: [
      {
        name: "nodeCa",
        children: [
          {
            name: "nodeCa1",
            value: 8,
          },
          {
            upperLabel: {
              show: true,
              color: "#fff",
              height: 30,
            },
            name: "nodeCa2",
            children: [
              {
                name: "nodeCa2a1",
                value: 3,
              },
              {
                name: "nodeCa2a2",
                value: 1,
              },
              {
                name: "nodeCa2a3",
                value: 1,
              },
              {
                name: "nodeCa2a4",
                value: 3,
              },
            ],
          },
          {
            name: "nodeCa3",
            value: 4,
          },
        ],
      },
    ],
  },
]);

const ttFormatter = (info) => {
  var value = info.value;
  var treePathInfo = info.treePathInfo;
  var treePath = [];
  for (var i = 1; i < treePathInfo.length; i++) {
    treePath.push(treePathInfo[i].name);
  }
  return [
    '<div class="tooltip-title">' +
    // echarts.format.encodeHTML(treePath.join("/")) +
    treePath.join("/") +
    "</div>",
    "Value: " + String(value) + " Unit",
    //    "Value: " + echarts.format.addCommas(value) + " KB",
  ].join("");
};

const chartOptions = ref({
  title: {
    text: props.dataName,
    left: 'center'
  },
  tooltip: {
    formatter: ttFormatter
  },
  backgroundColor: "#ddd",
  series: [
    {
      type: "treemap",
      itemStyle: {
        borderColor: "#444",
        borderWidth: 3,
        gapWidth: 5,
      },
      emphasis: {
        itemStyle: {
          borderColor: '#888',
        }
      },
      label: {
        show: true,
        formatter: "{b}\n{c}",
      },
      upperLabel: {
        show: false,
      },
      data: chartData.value,
    },
  ],
});

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

/* 
import * as echarts from 'echarts';

var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

option = {
  tooltip: {
    formatter: function (info) {
      var value = info.value;
      var treePathInfo = info.treePathInfo;
      var treePath = [];
      for (var i = 1; i < treePathInfo.length; i++) {
        treePath.push(treePathInfo[i].name);
      }
      return [
        '<div class="tooltip-title">' +
          echarts.format.encodeHTML(treePath.join('/')) +
          '</div>',
        'Value: ' + echarts.format.addCommas(value) + ' KB'
      ].join('');
    }
  },
  series: [
    {
      type: 'treemap',
      itemStyle: {
        borderColor: '#707',
        borderWidth: 2,
        gapWidth: 5
      },
      label: {
        show: true,
        formatter: '{b}\n{c}'
      },
      data: []
    }
  ]
};

option && myChart.setOption(option);
 */
</script>

<template>
  <v-chart v-if="dataLoaded" ref="theChart" :option="chartOptions" :style="{ height: '100%' }" :theme="chartTheme"
    :init-options="{ renderer: 'canvas' }" autoresize :aria-label="ariaLabel" @ready="onChartReady">
  </v-chart>
</template>

<style scoped>
.chart-template {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
