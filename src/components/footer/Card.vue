<template>
  <VaCard class="footerCard">

      <VaListItem v-if="supportPresent" class="list__item supported_by"
      :href="cardMessages[locale].supported_by_url"
      target="_blank"
      >
        <VaListItemSection avatar style="max-width:60%;">
          <VaListItemLabel style="-webkit-line-clamp:unset;" class="supported_by_label">
            {{ cardMessages[locale].supported_by }}
          </VaListItemLabel>
        </VaListItemSection>

        <VaListItemSection>
          <VaAvatar size="large">
            <img
              :src="supportIcon"
              :alt="cardMessages[locale].supported_by_long"
              :ariaLabel="cardMessages[locale].supported_by_long"
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

// name für i18n key
const props = defineProps({
  name: {
    type: String,
    default: "card",
  },
});
console.log("Card name:", props.name);

// read config
import cardConfig from "./card.json"
// check support present for subsequent display of support info 
const supportPresent = (cardConfig.support && cardConfig.support.present) || false
const supportIcon = "/images/" + cardConfig.support.icon

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

  for (const key in cardContent) {
    if (!supportedLanguages.includes(key)) continue;
    content.value[key] = cardContent[key];
  }
});
</script>

<style scoped lang="scss">
@use "sass:color";
@use '@/style/colors.scss';
@use "vuestic-ui/styles/grid";

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
  border: solid 3px;
  border-radius: .5rem;
  border-color: light-dark(colors.$dash-border-light,colors.$dash-border-dark);

}

.supported_by_label {
  color: light-dark(colors.$black, colors.$white);
  font-size: 1.2rem;
  font-weight: bold;
}

</style>
