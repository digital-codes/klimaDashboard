<template>
    <div class="container">
        <div class="category-values">
            <div v-for="category in categories" :key="category.name" :class="category.class">
                <h3>{{ category.name }}</h3>
                <p>{{ category.value }}</p>
            </div>
        </div>
        <div class="category-icons">
            <div v-for="category in categories" :key="category.name">
                <img :src="category.icon" :style="{ width: calculateIconSize(category.value) }" />
            </div>
        </div>
        <div class="slider">
            <input type="range" min="0" max="100" v-model="sliderValue" @input="updateCategoryValues" />
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const categories = ref([
    { name: 'Category 1', value: 10, icon: vite, class: "left"}, //'category1.png' },
    { name: 'Category 2', value: 20, icon: vue, class: "right"}, //'category2.png' },
]);

import vite from "../assets/vite.svg";  
import vue from "../assets/vue.svg";  

const sliderValue = ref(50);

const updateCategoryValues = () => {
    categories.value[0].value = sliderValue.value;
    categories.value[1].value = 100 - sliderValue.value;
    /*
    categories.value.forEach((category) => {
        category.value = Math.floor(Math.random() * 100);
    });
    */
};


const calculateIconSize = (value) => {
    const maxCategoryValue = 100
    const ratio = value / maxCategoryValue;
    const baseSize = 50; // Change this to adjust the base size of the icons
    const maxSize = 100; // Change this to adjust the maximum size of the icons
    return `${baseSize + (maxSize - baseSize) * ratio}px`;
};

onMounted(() => {
    updateCategoryValues();
}); 

</script>

<style scoped>

.container {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr 1fr;
    gap: 10px;
}

.category-values {
    grid-column: 1;
    grid-row: 1;
    display: grid;
    grid-template-rows: 1fr; ;
    grid-template-columns:  1fr 1fr;
    gap: 10px;
}
.category-values .right{
    grid-column: 2;
    gap: 10px;
}

.category-icons {
    grid-column: 1;
    grid-row: 2;
    display: grid;
    grid-template-rows: 1fr;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}
.category-icons .right{
    grid-column: 2;
    gap: 10px;
}

.slider {
    grid-column: 1;
    grid-row: 3;
    display: grid;
    grid-template-rows: 1fr;
    grid-template-columns:  repeat(auto-fit, minmax(0, 1fr));
    gap: 10px;
}

/*
.category-values {
    grid-column: 1;
    grid-row: 1;
    display: grid;
    grid-template-columns: 1fr; ;
    grid-template-rows:  repeat(auto-fit, minmax(0, 1fr));
    gap: 10px;
}
.category-values .right{
    grid-column: 2;
    gap: 10px;
}

.category-icons {
    grid-column: 1;
    grid-row: 2;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows:  repeat(auto-fit, minmax(0, 1fr));
    gap: 10px;
}
.category-icons .right{
    grid-column: 2;
    gap: 10px;
}


*/
.category-icons img {
    object-fit: contain;
}
</style>
