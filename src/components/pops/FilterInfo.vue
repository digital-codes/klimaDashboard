<template>
<VaModal
    v-model="showModal"
    hide-default-actions="true"
    close-button
  >
    <h3 class="va-h3">
      {{ props.name }}
    </h3>
    <p class="item" v-for="(item,index) in props.content.split('\n')" :key="index">{{ item }}</p>
    <a v-if="props.link > ''" :href="props.link" target="_blank" class="va-link">Learn more</a>
  </VaModal>
</template>

<script setup>
import { ref, watch } from 'vue'   
const props = defineProps({
  name: String,
  content: Object,
  link: {
    String,
    default: 'https://www.cern.ch'
  },
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

<style scoped>
.item {
  margin-bottom: 10px;
}
.va-link .link {
  color: #0072c6;
  text-decoration: none;
}
</style>
