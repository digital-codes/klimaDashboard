<template>
<HomeCard name="home" />
</template>

<script setup>
import { defineAsyncComponent } from 'vue'
const HomeCard = defineAsyncComponent(() => import("@/components/home/Card.vue"))

</script>
