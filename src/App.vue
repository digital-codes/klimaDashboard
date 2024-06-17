<script setup>
// 1i8n at top !
import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales } = useI18n();

import { useConfigStore } from './services/configStore';
const configStore = useConfigStore();

import CardTemplate from "./components/tiles/dummy/CardTemplate.vue"

import HeaderCard from "./components/header/HeaderCard.vue"

import { ref, watch, onMounted } from 'vue';
import { useBreakpoint } from 'vuestic-ui';

/* theme switch: https://ui.vuestic.dev/styles/colors */
import { computed } from 'vue';
import { useColors } from "vuestic-ui";

// mode switch 
const { applyPreset, currentPresetName } = useColors();

const modeSwitch = computed({
  get() {
    return currentPresetName.value
  },
  set(value) {
    applyPreset(value)
    // set color-scheme for non-vuestic components
    if (value === "dark") {
      document.body.style["color-scheme"] = "dark"
    } else {
      document.body.style["color-scheme"] = "light"
    }
  }
})


// ----------------------------


const showSidebar = ref(false)

const breakpoints = useBreakpoint()

const switchValue = ref(false)

const langSel = ref("")
//locale.value = langSel
console.log(availableLocales)
const languages = availableLocales

const appContainer = ref(null)

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


</script>


<template>
  <VaLayout ref="appContainer" :left="{ absolute: breakpoints.smDown }">
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
          <div class="langselect">
            <VaSelect v-model="langSel" :options="languages" :placeholder="configStore.getCurrentLocale">
              <template #prepend>
                <VaIcon name="translate" class="xlate" />
              </template>
            </VaSelect>
          </div>
          <VaButton round :icon="modeSwitch == 'dark' ? 'dark_mode' : 'light_mode'"
            @click="modeSwitch = modeSwitch == 'dark' ? 'light' : 'dark'" />
          <!-- 

  <VaSwitch
      v-model="modeSwitch"
      true-value="dark" false-value="light"
      color="#5123a1"
      off-color="#ffd300"
      style="--va-switch-checker-background-color: #252723;"
    >
      <template #innerLabel>
        <div class="va-text-center">
          <VaIcon
            :name="modeSwitch ? 'dark_mode' : 'light_mode'"
          />
        </div>
      </template>
    </VaSwitch>
    -->

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
        <HeaderCard name="header"/>
        <!-- 
        <h3 class="va-h3">Size Animation </h3>
        -->
        <CardTemplate name="dummy" class="tile" />
      </main>
    </template>
  </VaLayout>
</template>

<style scoped>
main {
  padding: 20px;
}

.langselect {
  max-width: 6rem;
  ;
}

.xlate {
  margin-left: .5rem;
  margin-right: .5rem;
}
</style>
