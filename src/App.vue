<script setup>
// 1i8n at top !
import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales } = useI18n();

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import { ref, watch, onMounted, onUnmounted, computed } from 'vue';

import { useBreakpoint } from 'vuestic-ui';

/* theme switch: https://ui.vuestic.dev/styles/colors */
import { useColors } from "vuestic-ui";

import { useRouter } from 'vue-router';
const router = useRouter();

import FooterCard from "@/components/footer/Card.vue"


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
    configStore.setTheme(value);
  }
})

// ----------------------------

import logo from "@/assets/logos/logo.png"

const breakpoints = useBreakpoint()

const langSel = ref("")
//locale.value = langSel
console.log(availableLocales)
const languages = availableLocales

const appContainer = ref(null)

// ----------------------------
const showSidebar = ref(false)

const menuToggle = () => {
  showSidebar.value = !showSidebar.value
};

const goto = (path) => {
  console.log("goto", path)
  router.push(path)
  showSidebar.value = false
}

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

// custom scroll stuff due to VaBacktoTop not working
const bttVisible = ref(true)
onMounted(() => {
  window.addEventListener('scroll', handleScroll, {passive: true});
});
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
const handleScroll = () => {
  bttVisible.value = window.scrollY > 300;
};
const scoll2top = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

</script>


<template>
  <VaLayout ref="appContainer" :left="{ absolute: breakpoints.smDown }">
    <template #top>
      <VaNavbar color="primary" class="py-2" fixed>
        <template #left>
          <VaButton :icon="showSidebar ? 'menu_open' : 'menu'" @click="menuToggle()" size="large" 
            title="Open sidebar menu" 
            role="switch"
            :aria-checked="showSidebar? 'true' : 'false'"
        />
        </template>
        <template #center>
          <VaNavbarItem role="link" aria-label="Click for Home">
            <VaImage :src="logo" 
            title="Dashboard Logo. Click for 'Home'" 
            fit="fit" class="logoimg" 
            @click="router.push({ name: 'Home' })"
            ></VaImage>
          </VaNavbarItem>
        </template>
        <template #right>
          <div class="langselect">
            <VaSelect 
              contentClass="selection" 
              v-model="langSel" 
              :options="languages" 
              :placeholder="configStore.getCurrentLocale"
            >
              <template #prepend>
                <VaIcon name="translate" class="xlate" />
              </template>
            </VaSelect>
          </div>
          <VaButton round :icon="modeSwitch == 'dark' ? 'dark_mode' : 'light_mode'"
            @click="modeSwitch = modeSwitch == 'dark' ? 'light' : 'dark'" 
            title="Switch to dark mode" 
            role="switch"
            :aria-checked="modeSwitch == 'dark' ? 'true' : 'false'"
          />
        </template>
      </VaNavbar>
    </template>

    <template #left>
      <VaSidebar v-model="showSidebar">
        <VaSidebarItem @click="goto('/')" tabindex="0" role="link">
            <VaSidebarItemContent>
              <VaIcon class="material-icons-outlined" name="home" size="large" />
              <VaSidebarItemTitle>
                Home
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem @click="goto('/dash')" tabindex="0" role="link">
            <VaSidebarItemContent>
              <VaIcon class="material-icons-outlined" name="insert_chart" size="large" />
              <VaSidebarItemTitle>
                Dashboard
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem @click="goto('/imprint')" tabindex="0" role="link">
            <VaSidebarItemContent>
              <VaIcon class="material-icons-outlined" name="info" size="large" />
              <VaSidebarItemTitle>
                Imprint
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem @click="goto('/gdpr')" tabindex="0" role="link">
            <VaSidebarItemContent>
              <VaIcon class="material-icons-outlined" name="privacy_tip" size="large" />
              <VaSidebarItemTitle>
                Gdpr
              </VaSidebarItemTitle>
            </VaSidebarItemContent>
        </VaSidebarItem>
      </VaSidebar>
    </template>


    <template #content>
      <main class="p-4" id="main">

        <router-view />

        <FooterCard name="footer" id="df" />

        <!-- custom scroll to top -->
        <VaButton v-if="bttVisible" 
        class="btt-button" 
        @click="scoll2top" 
        aria-controls="back to top" aria-label="Go to top">
          <VaIcon name="keyboard_arrow_up" size="medium"/>
        </VaButton>

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

.btt-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
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

.logoimg:hover {
  width: 5rem;
  cursor: pointer; 
}

.va-sidebar__title {
  text-align: left;
  margin-left: 1rem;
}


</style>

<style>

</style>
