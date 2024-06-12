<script setup>
// 1i8n at top !
import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales } = useI18n();

import { useConfigStore } from './services/configStore';
const configStore = useConfigStore();

import HelloWorld from './components/HelloWorld.vue'
import SizeAnimation from "./components/SizeAnimation.vue"

import CardTemplate from "./components/CardTemplate.vue"

import { ref, watch, onMounted } from 'vue';
import { useBreakpoint } from 'vuestic-ui';

const showSidebar = ref(false)

const breakpoints = useBreakpoint()

const switchValue = ref(false)

const langSel = ref("")
//locale.value = langSel
console.log(availableLocales)
const languages = availableLocales

console.log(langSel.value)
console.log(locale.value)

watch(langSel, (newValue, oldValue) => {
  // Code to execute when langSel changes
  console.log(newValue)
  configStore.setCurrentLocale(newValue);
  locale.value = newValue
});

onMounted(() => {
  // Code to execute when the component is mounted
  console.log('mounted')
  const lang = configStore.getCurrentLocale
  console.log(lang)
  locale.value = lang
  langSel.value = lang
  console.log(locale.value)
  console.log(langSel.value)

});

/*

watch(() => configStore.currentLocale, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    import(`./locales/${newValue}.json`).then((messages) => {
      i18n.global.setLocaleMessage(newValue, messages.default || messages);
      i18n.global.locale = newValue;
    });
  }
});
*/


</script>


<template>
  <VaLayout 
    :left="{ absolute: breakpoints.smDown }"
  >
    <template #top>
      <VaNavbar color="primary" class="py-2">
        <template #left>
          <VaButton :icon="showSidebar ? 'menu_open' : 'menu'" @click="showSidebar = !showSidebar" />
        </template>
        <template #center>
          <VaNavbarItem class="font-bold text-lg">
            LOGO
          </VaNavbarItem>
        </template>
        <template #right>
 <div class="max-w-xs">
    <VaLabel>{{ $t('langsel') }}</VaLabel>
    <VaSelect
      v-model="langSel"
      :options="languages"
      :placeholder="configStore.getCurrentLocale"
    />
  </div>
      </template>
      </VaNavbar>
    </template>

    <template #left>
      <VaSidebar v-model="showSidebar">
        <VaSidebarItem>
          <VaSidebarItemContent>
            <VaIcon name="home" /> 
            <VaSidebarItemTitle>
              Home
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem>
          <VaSidebarItemContent>
            <VaIcon name="phone" />
            <VaSidebarItemTitle>
              About
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
      </VaSidebar>
    </template>

    <template #content>
      <main class="p-4">
        <h3 class="va-h3">Size Animation </h3>
        <!-- 
          <SizeAnimation></SizeAnimation>
        -->
        <CardTemplate />
        <VaSwitch
      v-model="switchValue"
      color="#5123a1"
      off-color="#ffd300"
      style="--va-switch-checker-background-color: #252723;"
    >
      <template #innerLabel>
        <div class="va-text-center">
          <VaIcon
            :name="switchValue ? 'dark_mode' : 'light_mode'"
          />
        </div>
      </template>
    </VaSwitch>

    </main>
    </template>
  </VaLayout>
</template>

<style scoped>
main {
  padding: 20px;
}


</style>
