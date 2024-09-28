<template>
    <VaDataTable class="tablechart" v-if="dataLoaded" ref="theChart" :items="data" :columns="datakeys" sticky-header
        height="100%">
    </VaDataTable>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { nextTick } from 'vue';

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

// data parser
import Papa from 'papaparse';

import { useColors } from "vuestic-ui";
const { currentPresetName } = useColors();


const props = defineProps({
    /* Add your props here */
    dataUrl: {
        type: String,
        required: true,
    },
    ariaLabel: {
        type: String,
        default: "Aria LineChart",
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
    }
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


watch(() => props.dataUrl, async (newValue, oldValue) => {
    console.log("Data URL changed:", newValue);
    await loadData();

});

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
        } else { // assume csv
            const csvString = await response.text();
            Papa.parse(csvString, {
                header: true,
                dynamicTyping: true,
                delimiter: props.dataDelimiter,
                complete: function (results) {
                    console.log("CSV parsed:", results.data);
                    data.value = results.data;
                }
            });
        }
        // empty columns array will add all keys
        for (const key in data.value[0]) {
            if (props.dataColumns.length === 0 || props.dataColumns.includes(key)) {
                datakeys.value.push(key);
            }
        }
        // va-table shows all columns if keys are empty. So we need to set prevent display if no keys
        dataLoaded.value = datakeys.value.length > 0;
        await nextTick();
        console.log("Data loaded");
        if (datakeys.value.length == 0) {
            alert("No valid columns");
        }
    } catch (error) {
        console.error("Failed to load chart data:", error);
    }
}

onMounted(async () => {

    await loadData();
    console.log("config theme:", configStore.getTheme)
    if (configStore.getTheme == "dark") {
        console.log("Dark theme detected")
    } else {
        console.log("Light theme detected")
    }
});

</script>


<style scoped>
.tablechart {
    --va-data-table-thead-font-size: .9rem;
    --va-scroll-color: #000;
    --va-scrollbar-size: 10px;
}

/* Works on Firefox */
.tablechart {
    scrollbar-width: .5rem;
    scrollbar-color: blue orange;
}

/* Works on Chrome, Edge, and Safari */
.tablechart::-webkit-scrollbar {
    width: .5rem;
    scrollbar-color: blue orange;
}
</style>

<style></style>
