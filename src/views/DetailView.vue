<template>
<DetailCard name="Detail" :topic="topic" />
</template>

<script setup>
import { defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const topic = route.params.topic || 'default'

const DetailCard = defineAsyncComponent(() => import("@/components/detail/Card.vue"))

</script>
