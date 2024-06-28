<template>
        <v-chart v-if="dataLoaded" ref="theChart" :option="chartOptions" :style="{ height: '100%' }" :theme="chartTheme"
            autoresize></v-chart>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { nextTick } from 'vue';

//import pkw from "@/assets/icons/ModalSplit/MS_Klimadashboard_Icons_m_modalsplit_pkw.svg?url";
import pkw from "@/assets/icons/generated/car.svg?url";
import pkw2 from "@/assets/logos/generated/bikes_white_on_transparent.svg?url"
// import bus from "@/assets/icons/ModalSplit/MS_Klimadashboard_Icons_m_modalsplit_bus.svg?url";
import bus from "@/assets/icons/generated/house.svg?url";
import bus2 from "@/assets/logos/generated/fossils_white_on_transparent.svg?url";


const updateCategoryValues = (val) => {
    const maxScale = 100
    chartOptions.value.series[0].data[0].symbolSize = maxScale - val
    chartOptions.value.series[0].data[1].symbolSize = val 
};

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

// ----------------- Chart -----------------
import VChart from "vue-echarts";

import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
// normally, only a single chart type is needed
// unless toolbox allows to switch types (like here ...)
import { PictorialBarChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
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
    range: {
        type: Number,
        default: 50
    },
    animate : {
        type: Boolean,
        default: false
    },
});


watch(currentPresetName, (newValue, oldValue) => {
    if (newValue == "dark") {
        chartOptions.value.series[0].data[0].symbol = "image://" + pkw2
        chartOptions.value.series[0].data[1].symbol = "image://" + bus2
    } else {
        chartOptions.value.series[0].data[0].symbol = "image://" + pkw
        chartOptions.value.series[0].data[1].symbol = "image://" + bus
    }
});

watch(() => props.range, (newValue, oldValue) => {
    updateCategoryValues(newValue)
});


const theChart = ref(null);
const chartTheme = ref(currentPresetName) // already reactive. don't watch for theme

const dataLoaded = ref(false);

const chartOptions = ref({
    title: {
        show: true,
        text: "Pictorial graph example",
        left: "center",
        top: 10,
    },
    tooltip: {
        show:true,
        formatter: function (param) {
            const size = param.data.symbolSize
                return String(size);
            },
    },
    xAxis: {
        type: "category",
        data: ["Left", "Right"],
        axisTick: {
            show: false
        },
        axisLabel: {
            interval: 0
        },
        show:false
    },
    yAxis: {
        max: 100,
        show: false
    },
    series: [
        {
            type: 'pictorialBar',
            name: 'S1',
            animationDuration: 0,
            label: {
                show: true,
                position: 'top',
                formatter: function (param) {
                    const size = param.data.symbolSize
                    return size;
                },
                offset: [0, -20],
                fontSize: 18,
            },
            // symbol: "image://" + pkw,  only needed for legend
            z: 10,
            data: [
                {
                    value: 5,
                    symbolPosition: 'center',
                    symbolSize: 5,
                    symbol: "image://" + pkw,
                },
                {
                    value: 5,
                    symbolPosition: 'center',
                    symbolSize: 5,
                    symbol: "image://" + bus,
                },
            ]
        },
    ]
}
)

use([
    CanvasRenderer,
    PictorialBarChart,
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent
]);


onMounted(async () => {

    try {
        console.log("Fetching: ", props.chartDataUri);
        const response = await fetch(props.chartDataUri);
        const data = await response.text();
        dataLoaded.value = true;
        await nextTick();
        console.log("Data loaded:", data);
        updateCategoryValues()
        console.log("config theme:", configStore.getTheme)
        if (configStore.getTheme == "dark") {
            chartOptions.value.series[0].data[0].symbol = "image://" + pkw2
            chartOptions.value.series[0].data[1].symbol = "image://" + bus2
        } else {
            chartOptions.value.series[0].data[0].symbol = "image://" + pkw
            chartOptions.value.series[0].data[1].symbol = "image://" + bus
        }
        updateCategoryValues(props.range)
    } catch (error) {
        console.error("Failed to load chart data:", error);
    }
});

</script>

<style scoped>
.chart-template {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
