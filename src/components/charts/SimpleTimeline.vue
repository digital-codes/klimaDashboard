<script setup>
import { ref, onMounted, watch, onUnmounted } from "vue";
import { nextTick } from "vue";

import VChart, { UPDATE_OPTIONS_KEY } from "vue-echarts";

import { useConfigStore } from "@/services/configStore";
const configStore = useConfigStore();

// breakpoint
import { useBreakpoint } from "vuestic-ui";
const breakpoint = useBreakpoint();

import {graphic} from 'echarts'

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
import { CustomChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
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
    default: "Aria Timeline",
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
const data = ref([]);
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
  //data.value = chartData.value;
  const chartData = []
  for (const milestone of milestones) {
            var categoryIndex = categories.indexOf(milestone.category);
            chartData.push({
                name: milestone.name,
                value: [categoryIndex, milestone.start, milestone.start + milestone.duration, milestone.duration],
                itemStyle: {
                    normal: {
                        color: colors[categoryIndex]
                    }
                }
            });
        };
  data.value = chartData;
  console.log("Data loaded:", data.value);
  await nextTick();
  dataLoaded.value = true
  chartOptions.value.series[0].data = data.value;
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
};

use([
  CanvasRenderer,
  SVGRenderer,
  CustomChart,
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
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

const colors = ['#7b9ce1', '#bd6d6c', '#75d874', '#e0bc78']
const categories = ['Entscheidungen', 'Veranstaltungen', 'Einreichungen'];
const milestones = [
  { name: 'Beschluss zur Erstellung', category: 'Entscheidungen', start: new Date('2020-01-01').getTime(), duration: 10 },
  { name: 'Klimaforum abgehalten', category: 'Veranstaltungen', start: new Date('2023-09-01').getTime(), duration: 30 },
  { name: 'Entwurf vorgestellt', category: 'Veranstaltungen', start: new Date('2023-10-04').getTime(), duration: 15 },
  { name: 'Genehmigung durch den Stadtrat', category: 'Entscheidungen', start: new Date('2023-11-28').getTime(), duration: 10 },
  { name: 'Einreichung beim Land', category: 'Einreichungen', start: new Date('2023-12-31').getTime(), duration: 20 },
  { name: 'Bestätigung der Wärmeplanung', category: 'Einreichungen', start: new Date('2024-04-01').getTime(), duration: 10 },
//  { name: 'Klimaneutralität erreicht', category: 'Ziele', start: new Date('2040-01-01').getTime(), duration: 365 }
];

const startTime = milestones[0].start - 365*24*3600*1000;
const endTime = milestones[milestones.length - 1].start + 365*24*3600*1000;


const renderItem = (params, api) => {
  var categoryIndex = api.value(0);
  var start = api.coord([api.value(1), categoryIndex]);
  var end = api.coord([api.value(2), categoryIndex]);
  var height = api.size([0, 1])[1] * 0.6;
  var width = Math.max(10, end[0] - start[0]); // Ensure a minimum width
  var rectShape = graphic.clipRectByRect(
    {
      x: start[0],
      y: start[1] - height / 2,
      width: width,
      height: height
    },
    {
      x: params.coordSys.x,
      y: params.coordSys.y,
      width: params.coordSys.width,
      height: params.coordSys.height
    }
  );
  return (
    rectShape && {
      type: 'rect',
      transition: ['shape'],
      shape: rectShape,
      style: api.style()
    }
  );
}

const ttFormatter = (params) => {
  return params.marker + params.name + ': ' + new Date(params.value[1]).toDateString();
}

const chartOptions = ref({
  title: {
    text: props.dataName,
    left: 'center'
  },

  tooltip: {
    formatter: ttFormatter
  },
  //backgroundColor: "#ddd",
  dataZoom: [
    {
      type: 'slider',
      filterMode: 'weakFilter',
      showDataShadow: false,
      //top: 400,
      labelFormatter: ''
    },
    {
      type: 'inside',
      filterMode: 'weakFilter'
    }
  ],
  grid: {
    //height: 200
  },
  xAxis: {
    min: startTime,
    max: endTime,
    scale: true,
    axisLabel: {
      formatter: function (val) {
        return new Date(val).getFullYear();
      }
    }
  },
  yAxis: {
    type: 'category',
    data: categories
  },
  series: [
    {
      type: 'custom',
      renderItem: renderItem,
      itemStyle: {
        opacity: 1
      },
      encode: {
        x: [1, 2],
        y: 0
      },
      data: data.value
    }
  ]
});

/*
In the context of the custom series, encode specifies how dimensions of the data array are used.
For example, data might look like this:
[
    [categoryIndex, startTime, endTime, duration]
]

Here, each array represents:

    Index 0: Category (y-axis)
    Index 1: Start time (x-axis)
    Index 2: End time (x-axis)
    Index 3: Duration (tooltip or styling)
*/


onMounted(async () => {
  if (configStore.getTheme == "dark") {
    console.log("Dark theme detected");
  } else {
    console.log("Light theme detected");
  }

  await loadData();
  theChart.value.setOption(chartOptions.value);
  //updateOptions()
});

onUnmounted(() => {
  if (animTimer.value) {
    clearInterval(animTimer.value);
  }
});

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
