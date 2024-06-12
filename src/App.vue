<script setup>
import { useConfigStore } from './services/configStore';
const configStore = useConfigStore();

import HelloWorld from './components/HelloWorld.vue'
import SizeAnimation from "./components/SizeAnimation.vue"

import CardTemplate from "./components/CardTemplate.vue"

import { ref, watch } from 'vue';
import { useBreakpoint } from 'vuestic-ui';

import { i18n }  from 'vue-i18n';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();


const showSidebar = ref(false)

const breakpoints = useBreakpoint()

const switchValue = ref(false)

const langSel = ref(configStore.getCurrentLocale)
const languages = ["en","de","fr","es"]

watch(langSel, (newValue, oldValue) => {
  // Code to execute when langSel changes
  console.log(newValue)
  configStore.setCurrentLocale(newValue);
  console.log("i18n",i18n.global)
  //t.global.locale = newValue;
  console.log("Select: ",t('langsel'))
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
