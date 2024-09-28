<template>
  <div style="text-align:left;">
    <VaButton class="backButton" @click="back" icon="arrow_back" color="primary" size="large" round></VaButton>
  </div>

  <VaCard class="detailCard">
    <div class="flex xs12">
      <div class="mdcontent fullheight" v-html="content"></div>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { locale } = useI18n();
import { onMounted, ref, watch } from "vue";
import { useRouter } from 'vue-router';
const router = useRouter();
const content = ref("");

// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  },
  topic: {
    type: String,
    required: true
  }
});

console.log("Card name:", props.name);

const errorMsg = {
  de: "Fehler beim Laden des Inhalts",
  en: "Error loading content"
};

const back = () => {
  router.go(-1)
};

watch(() => props.topic, () => {
  fetchContent();
});

watch(locale, () => {
  fetchContent();
});


const fetchContent = async () => {
  console.log("Fetching content for topic:", props.topic, locale.value);
  try {
    //const response = await fetch(`http://localhost:9000/php/details.php`, {
    const response = await fetch(`/php/details.php`, {
      method: 'POST',
      headers: {
        'Accept': 'text/html',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        topic: props.topic,
        lang: locale.value
      })
    });
    if (response.status === 200) {
      content.value = await response.text();
    } else {
      console.error('Failed to fetch content:', response.status);
      content.value = errorMsg[locale.value];
    }
  } catch (error) {
    console.error('Error fetching content:', error);
    content.value = errorMsg[locale.value];
  }
};

onMounted(() => {
  fetchContent();
});
</script>

<style scoped>
/* Add your card styles here */

.detailCard {
  margin: .5rem 0 .5rem 0;
  padding: .5rem;
  text-align: left;
  display: flex;
  flex-wrap: wrap;
}
</style>
