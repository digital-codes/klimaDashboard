<template>
<VaModal
    v-model="showModal"
    hide-default-actions="true"
    close-button
  >
    <h3 class="va-h3">
      {{ props.name }}
    </h3>
    <p>{{ props.content }}</p>
  </VaModal>
</template>

<script setup>
import { ref, watch } from 'vue'   
const props = defineProps({
  name: String,
  content: Object,
  open: {
    type: Boolean,
    default: false
  }
})

const showModal = ref(false)

watch(() => props.open, (newVal, oldVal) => {
    console.log("Open:", newVal) 
  if (newVal) {
    showModal.value = true
  } else {
    showModal.value = false
  }
})


</script>

