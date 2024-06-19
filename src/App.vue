<script setup>
// 1i8n at top !
import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales } = useI18n();

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import { ref, watch, onMounted, computed } from 'vue';
import { defineAsyncComponent } from 'vue'

import { useBreakpoint } from 'vuestic-ui';

/* theme switch: https://ui.vuestic.dev/styles/colors */
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

import logo from "@/assets/logos/logo.png"

const breakpoints = useBreakpoint()

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

const removeTag = (tag) => {
  currentTags.value = currentTags.value.filter(item => item !== tag);
}
const insertTag = (tag) => {
  // make sure we donÄt get duplicates
  currentTags.value = currentTags.value.filter(item => item !== tag);
  currentTags.value.push(tag)
}

const filterTag = (tag) => {
  if (currentTags.value.includes(tag)) {
    removeTag(tag)
  } else {
    insertTag(tag)
  }
}

</script>


<template>
  <VaLayout ref="appContainer" :left="{ absolute: breakpoints.smDown }">
    <template #top>
      <VaNavbar color="primary" class="py-2" fixed>
        <template #left>
          <VaButton :icon="showSidebar ? 'menu_open' : 'menu'" @click="showSidebar = !showSidebar" />
        </template>
        <template #center>
          <VaNavbarItem>
            <VaImage :src="logo" alt="Logo" fit="fit" class="logoimg"></VaImage>
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
        </template>
      </VaNavbar>
    </template>

    <template #left>
      <VaSidebar v-model="showSidebar">
        <VaSidebarItem>
          <router-link to="/">
            <VaSidebarItemContent>
              <VaIcon name="home" size="large" />
              <VaSidebarItemTitle>
                Home
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </router-link>
        </VaSidebarItem>
        <VaSidebarItem>
          <router-link to="/data">
            <VaSidebarItemContent>
              <VaIcon name="insert_chart" size="large" />
              <VaSidebarItemTitle>
                Data
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </router-link>
        </VaSidebarItem>
        <VaSidebarItem>
          <router-link to="/imprint">
            <VaSidebarItemContent>
              <VaIcon name="info" size="large" />
              <VaSidebarItemTitle>
                Imprint
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </router-link>
        </VaSidebarItem>
        <VaSidebarItem>
          <router-link to="/gdpr">
            <VaSidebarItemContent>
              <VaIcon name="privacy_tip" size="large" />
              <VaSidebarItemTitle>
                Gdpr
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
          </router-link>
        </VaSidebarItem>
      </VaSidebar>
    </template>


    <template #content>
      <main class="p-4" id="main">

        <router-view />

        <VaBacktop @click="console.log('backtop clicked')" vertical-offset="5rem" horizontal-offset="2rem"
          horizontal-position="right" vertical-position="bottom" visibility-height="1" speed="100">
        </VaBacktop>

      </main>

    </template>

  </VaLayout>
</template>

<style>
/* with fixed navbar we need some margin */
.va-layout__area--top {
  margin-bottom: 3rem;
}
</style>

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

.logoimg {
  width: 4rem;
}

.va-sidebar__title {
  text-align: left;
  margin-left: 1rem;
}
</style>
