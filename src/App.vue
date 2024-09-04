<script setup>
// 1i8n at top !
import { useI18n } from 'vue-i18n';
const { t, messages, locale, availableLocales } = useI18n();

import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();

import { ref, watch, onMounted, onUnmounted, computed, onBeforeMount } from 'vue';

import { useBreakpoint } from 'vuestic-ui';

/* theme switch: https://ui.vuestic.dev/styles/colors */
import { useColors } from "vuestic-ui";

import { useRouter } from 'vue-router';
const router = useRouter();

import FooterCard from "@/components/footer/Card.vue"

// read localized sidebar links
import cardMessages from "@/components/sidebar/lang.json";

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
configStore.setLanguages(languages)

const appContainer = ref(null)

// ----------------------------
const showSidebar = ref(false)
const msgsLoaded = ref(false)


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

onBeforeMount(async () => {
  // Code to execute when the component is mounted
  // localized content
  const supportedLanguages = availableLocales // use like so only in app.vue

  console.log("cardmsgs:", cardMessages)
  // localization data. save und "app" key
  for (const key in cardMessages) {
    if (!supportedLanguages.includes(key)) continue;
    console.log("Lang Msg", key)
    messages.value[key]["sidebar"] = cardMessages[key];
  }
  console.log("msgs", messages.value)
  msgsLoaded.value = true
})

onMounted(() => {
  // Code to execute when the component is mounted
  console.log('mounted')
  const lang = configStore.getCurrentLocale
  console.log(lang)
  locale.value = lang
  langSel.value = lang
  console.log(locale.value)
  console.log(langSel.value)
  // try to get color prefs on mount. else we might get mix of dark and light
  // until first switch toggle
  try {
    const colorPref = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    console.log("Initially:", colorPref === "dark" ? "dark" : "light")
    modeSwitch.value = colorPref
    configStore.setTheme(colorPref);
  } catch (e) {
    console.log("color prefs not avsailable")
  }

});

// custom scroll stuff due to VaBacktoTop not working
const bttVisible = ref(true)
onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true });
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


const mlist1 = ref([true]) // accordion open state

</script>


<template>
  <VaLayout ref="appContainer" :left="{ absolute: breakpoints.smDown }">
    <template #top>
      <VaNavbar color="primary" class="py-2" fixed>
        <template #left>
          <VaButton :icon="showSidebar ? 'menu_open' : 'menu'" @click="menuToggle()" size="large" :title="t('menu')"
            role="switch" :aria-checked="showSidebar ? 'true' : 'false'" />
        </template>
        <template #center>
          <VaNavbarItem role="link" aria-label="Click for Home">
            <VaImage :src="logo" :title='t("logo")' fit="fit" class="logoimg" @click="router.push({ name: 'Home' })">
            </VaImage>
          </VaNavbarItem>
        </template>
        <template #right>
          <div class="langselect">
            <VaSelect contentClass="selection" v-model="langSel" :options="languages"
              :placeholder="configStore.getCurrentLocale">
              <template #prepend>
                <VaIcon name="translate" class="xlate" />
              </template>
            </VaSelect>
          </div>
          <VaButton round :icon="modeSwitch == 'dark' ? 'dark_mode' : 'light_mode'"
            @click="modeSwitch = modeSwitch == 'dark' ? 'light' : 'dark'" :title='t("mode")' role="switch"
            :aria-checked="modeSwitch == 'dark' ? 'true' : 'false'" />
        </template>
      </VaNavbar>
    </template>

    <template #left>
      <VaSidebar v-model="showSidebar" v-if="msgsLoaded">
        <VaSidebarItem @click="goto('/')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="home" size="large" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.home") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>

        <VaSidebarItem @click="goto('/dash1')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="insert_chart" size="large" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.dash1") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>

        <!-- 
        <VaSidebarItem>
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="insert_chart" size="large" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.dash2") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>

        <VaSidebarItem @click="goto('/dash2_1')" tabindex="0" role="link" style="margin-left:1rem;">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="insert_chart" size="large" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.dash2_1") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem @click="goto('/dash2_2')" tabindex="0" role="link" style="margin-left:1rem;">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="insert_chart" size="large" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.dash2_2") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
        -->


        <VaSidebarItem>
          <VaSidebarItemContent style="display:flex; flex-direction: column;align-items:baseline;" @click="mlist1[0] = !mlist1[0]">
            <div style="display:flex;align-items:center;">
              <VaIcon class="material-icons-outlined" name="insert_chart" size="large"/>
            <VaSidebarItemTitle>
              {{ $t("sidebar.dash2") }}
            </VaSidebarItemTitle>
            <VaIcon class="material-icons-outlined" :name="mlist1[0]?'keyboard_arrow_up':'keyboard_arrow_down'" size="large"/>
          </div>
            <VaAccordion v-model="mlist1" style="flex-direction: column;align-items:baseline;">
              <VaCollapse>
                <template #body >
                  <VaSidebarItem @click="goto('/dash2_1')" tabindex="0" role="link" style="padding: 0;margin-left:1rem;">
                    <VaSidebarItemContent>
                      <VaIcon class="material-icons-outlined" name="insert_chart" size="large" />
                      <VaSidebarItemTitle>
                        {{ $t("sidebar.dash2_1") }}
                      </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                  </VaSidebarItem>
                  <VaSidebarItem @click="goto('/dash2_2')" tabindex="1" role="link" style="padding: 0;margin-left:1rem;">
                    <VaSidebarItemContent>
                      <VaIcon class="material-icons-outlined" name="insert_chart" size="large" />
                      <VaSidebarItemTitle>
                        {{ $t("sidebar.dash2_2") }}
                      </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                  </VaSidebarItem>
                </template>
              </VaCollapse>
            </VaAccordion>
          </VaSidebarItemContent>
        </VaSidebarItem>


        <VaSidebarItem @click="goto('/imprint')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="info" size="large" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.imprint") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem @click="goto('/gdpr')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="privacy_tip" size="large" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.gdpr") }}
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
        <VaButton v-if="bttVisible" class="btt-button" @click="scoll2top" :aria-controls="$t('totop')"
          :aria-label="$t('totop')">
          <VaIcon name="keyboard_arrow_up" size="medium" />
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
.va-collapse__header {
  display:none;
}


</style>
