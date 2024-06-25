<template>
    <div class="container">
        <v-chart v-if="dataLoaded" ref="theChart" :option="chartOptions" :style="{ height: '100%' }" :theme="chartTheme"
            autoresize></v-chart>
        <div class="slider">
            <input type="range" min="0" max="100" v-model="sliderValue" @input="updateCategoryValues" />
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

//import pkw from "@/assets/icons/ModalSplit/MS_Klimadashboard_Icons_m_modalsplit_pkw.svg?url";
import pkw from "@/assets/icons/generated/car.svg?url";
import pkw2 from "@/assets/logos/generated/bikes_white_on_transparent.svg?url"
// import bus from "@/assets/icons/ModalSplit/MS_Klimadashboard_Icons_m_modalsplit_bus.svg?url";
import bus from "@/assets/icons/generated/house.svg?url";
import bus2 from "@/assets/logos/generated/fossils_white_on_transparent.svg?url";


const sliderValue = ref(50);

const updateCategoryValues = () => {
    const scale = sliderValue.value / 20
    /* */
    chartOptions.value.graphic.elements[0].children[0].scaleX = 1 + scale
    chartOptions.value.graphic.elements[0].children[0].scaleY = 1 + scale
    chartOptions.value.graphic.elements[1].children[0].scaleX = 6 - scale
    chartOptions.value.graphic.elements[1].children[0].scaleY = 6 - scale
    /* */
    /*
    chartOptions.value.graphic.elements[0].children[0].style.width = 20 * (1 + scale)
    chartOptions.value.graphic.elements[0].children[0].style.height = 20 * (1 + scale)
    chartOptions.value.graphic.elements[1].children[0].style.width = 20 * (6 - scale)
    chartOptions.value.graphic.elements[1].children[0].style.height = 20 * (6 - scale)
    */
    // vue-echarts updates automatically from reactive options
    //theChart.value.setOption(chartOptions.value);

};

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

// ----------------- Chart -----------------
import VChart from "vue-echarts";

import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
// normally, only a single chart type is needed
// unless toolbox allows to switch types (like here ...)
import {
    TitleComponent,
    GraphicComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent
} from "echarts/components";

// optimize later
// import "echarts"

import { useColors } from "vuestic-ui";
import { nextTick } from 'vue';
const { currentPresetName } = useColors();

watch(currentPresetName, (newValue, oldValue) => {
    if (newValue == "dark") {
        chartOptions.value.graphic.elements[0].children[0].style.image = pkw2
        chartOptions.value.graphic.elements[1].children[0].style.image = bus2
    } else {
        chartOptions.value.graphic.elements[0].children[0].style.image = pkw
        chartOptions.value.graphic.elements[1].children[0].style.image = bus
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

// const chartOptions = ref({});

const dataLoaded = ref(false);

const chartOptions = ref({
    graphic: {
        elements: [
            {
                type: 'group',
                left: '10%',
                top: 'center',
                children: [
                    {
                        type: "image",
                        x: 0,
                        y: 0,
                        scaleX: 1,
                        scaleY: 1,
                        style: {
                            image: pkw,
                            x: 0,
                            y: 0,
                            width: 20,
                            height: 20,
                        },
                    },
                    // text not at fixed position
                    /*
                    {
                        type: 'text',
                        left: 'center',
                        top: "top",
                        z: 100,
                        style: {
                            fill: '#fff',
                            text: 'Left',
                            font: 'bold 26px sans-serif'
                        }
                    }
                    */
                ]
            },
            {
                type: 'group',
                right: '10%',
                top: 'center',
                children: [
                    {
                        type: "image",
                        x: 0,
                        y: 0,
                        scaleX: 1,
                        scaleY: 1,
                        style: {
                            image: bus,
                            x: 0,
                            y: 0,
                            width: 20,
                            height: 20,
                            color: "#ff0",
                        },
                    },
                ]
            },
            {
                    type: 'text',
                    left: 32,
                    top: "top",
                    z: 100,
                    style: {
                        fill: '#fff',
                        text: 'Left',
                        font: 'bold 18px sans-serif'
                    }
                    },
                    {
                    type: 'text',
                    right: 32,
                    top: "top",
                    z: 100,
                    style: {
                        fill: '#fff',
                        text: 'Right',
                        font: 'bold 18px sans-serif'
                    }
                    }
        ]
    }
}
)

use([
    CanvasRenderer,
    GraphicComponent,
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
            chartOptions.value.graphic.elements[0].children[0].style.image = pkw2
            chartOptions.value.graphic.elements[1].children[0].style.image = bus2
        } else {
            chartOptions.value.graphic.elements[0].children[0].style.image = pkw
            chartOptions.value.graphic.elements[1].children[0].style.image = bus
        }
    } catch (error) {
        console.error("Failed to load chart data:", error);
    }
});

</script>

<style scoped>
.container {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 2fr 1fr;
    gap: 10px;
    height: 100%;
}

.slider {
    grid-column: 1;
    grid-row: 2;
    display: grid;
    grid-template-rows: 1fr;
    grid-template-columns: repeat(auto-fit, minmax(0, 1fr));
    gap: 10px;
}

.chart-template {
    display: flex;
    justify-content: center;
    align-items: center;
    /*
    grid-column: 1;
    grid-row: 1;
    display: grid;
    grid-template-rows: 1fr;
    grid-template-columns: repeat(auto-fit, minmax(0, 1fr));
    gap: 10px;
    */
}
</style>
