<template>
<GdprCard name="gdpr" />
</template>

<script setup>
import { defineAsyncComponent } from 'vue'

import { useBreakpoint } from 'vuestic-ui';

/* theme switch: https://ui.vuestic.dev/styles/colors */
import { useColors } from "vuestic-ui";


const GdprCard = defineAsyncComponent(() => import("@/components/gdpr/Card.vue"))

</script>
