<template>
  <VaCard class="footerCard">

      <VaListItem class="list__item supported_by"
      :href="supported_by_url"
      target="_blank"
      >
        <VaListItemSection avatar style="max-width:60%;">
          <VaListItemLabel style="-webkit-line-clamp:unset;" class="supported_by_label">
            {{ $t("supported_by") }}
          </VaListItemLabel>
        </VaListItemSection>

        <VaListItemSection>
          <VaAvatar size="large">
            <img
              :src="supported"
              :alt="t('supported_by_long')"
              :ariaLabel="t('supported_by_long')"
            />
          </VaAvatar>
        </VaListItemSection>
      </VaListItem>

    <div class="flex xs12">
      <div class="mdcontent" v-html="content[locale]"></div>
    </div>

  </VaCard>
</template>

<script setup>
import { useI18n } from "vue-i18n";
const { messages, locale, t } = useI18n();
import { ref, onBeforeMount } from "vue";

import { useConfigStore } from "@/services/configStore";
const configStore = useConfigStore();

import { useBreakpoint } from "vuestic-ui";

import supported from "@/assets/images/support.png";
const supported_by_url = "https://www.karlsruhe.de/umwelt-klima/klimaschutz-klimawandel/klimaschutzkampagne"

// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  },
});
console.log("Card name:", props.name);

// read localized card content
import cardContent from "./text.json";

// read localized card messages
import cardMessages from "./lang.json";

// content pane
const content = ref({});

onBeforeMount(() => {
  // Code to execute when the component is mounted
  // Merge card specific messages with global
  // localized content
  const supportedLanguages = configStore.getLanguages;

  // localization data
  for (const key in cardMessages) {
    if (!supportedLanguages.includes(key)) continue;
    messages.value[key][props.name] = cardMessages[key];
  }

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;
    content.value[key] = cardContent[key];
  }
});
</script>

<style scoped>
/* Add your card styles here */

.footerCard {
  margin: 0.5rem 0 0.5rem 0;
  padding: 0.5rem;
  text-align: left;
  display: flex;
  flex-wrap: wrap;
}

.supported_by {
  margin-left:auto;
  margin-right:auto;
  padding:1rem;
}

.supported_by_label {
  color: light-dark(#000, #fff);
  font-size: 1.2rem;
  font-weight: bold;
}

</style>
