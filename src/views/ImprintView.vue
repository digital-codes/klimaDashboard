<template>
<ImprintCard name="imprint" />
</template>

<script setup>
import { defineAsyncComponent } from 'vue'
const ImprintCard = defineAsyncComponent(() => import("@/components/imprint/Card.vue"))

</script>
