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
      icons.value = {
        "icon1": icon1_d,
        "icon2": icon2_d,
        "icon3": icon3_d,
        "icon4": icon4_d,
        "icon5": icon5_d,
      }
    } else {
      document.body.style["color-scheme"] = "light"
      icons.value = {
        "icon1": icon1_l,
        "icon2": icon2_l,
        "icon3": icon3_l,
        "icon4": icon4_l,
        "icon5": icon5_l,
      }
    }
    configStore.setTheme(value);
  }
})

// ----------------------------
// load sidebar icons
import icon1_l from "@/assets/icons/dashboard/weather.svg?url"
import icon2_l from "@/assets/icons/dashboard/house.svg?url"
import icon3_l from "@/assets/icons/dashboard/protection.svg?url"
import icon4_l from "@/assets/icons/dashboard/emissions.svg?url"
import icon5_l from "@/assets/icons/dashboard/adaptation.svg?url"

import icon1_d from "@/assets/icons/dashboard/weather_d.svg?url"
import icon2_d from "@/assets/icons/dashboard/house_d.svg?url"
import icon3_d from "@/assets/icons/dashboard/protection_d.svg?url"
import icon4_d from "@/assets/icons/dashboard/emissions_d.svg?url"
import icon5_d from "@/assets/icons/dashboard/adaptation_d.svg?url"

const icons = ref({
  "icon1": icon1_l,
  "icon2": icon2_l,
  "icon3": icon3_l,
  "icon4": icon4_l,
  "icon5": icon5_l
})

// ----------------------------

//import logo from "@/assets/logos/logo.png"
import logo from "@/assets/icons/dashboard/climate_color_transparent_b.svg?url"

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
  // Set lang attribute dynamically
  document.documentElement.lang = locale.value;

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
          <VaNavbarItem v-if="breakpoints.mdUp"><span class="headline left">{{ $t("climate") }}</span></VaNavbarItem>
          <VaNavbarItem role="link" aria-label="Click for Home">
            <VaImage :src="logo" :title='t("logo")' fit="fit" class="logoimg" @click="router.push({ name: 'Home' })">
            </VaImage>
          </VaNavbarItem>
          <VaNavbarItem v-if="breakpoints.mdUp"><span class="headline right">Karlsruhe</span></VaNavbarItem>
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
      <VaSidebar v-model="showSidebar" v-if="msgsLoaded" width="20rem">
        <VaSidebarItem @click="goto('/')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="home" size="2rem" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.home") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>

        <VaSidebarItem @click="goto('/dash1')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaImage :src="icons.icon1" alt="Icon Weather and Climate" style="width:2rem;" />
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
          <VaSidebarItemContent style="display:flex; flex-direction: column;align-items:baseline;"
            @click="mlist1[0] = !mlist1[0]">
            <div style="display:flex;align-items:center;">
              <VaImage :src="icons.icon3" 
                alt="Icon Climate Protection" style="width:2rem;" />
              <VaSidebarItemTitle>
                {{ $t("sidebar.dash2") }}
              </VaSidebarItemTitle>
              <VaIcon class="material-icons-outlined" :name="mlist1[0] ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                size="large" />
            </div>
            <VaAccordion v-model="mlist1" style="flex-direction: column;align-items:baseline;margin-left:0;">
              <VaCollapse class="sidebar">
                <template #body>
                  <VaSidebarItem @click="goto('/dash2_1')" tabindex="0" role="link"
                    style="padding: 0;margin-left:1rem;">
                    <VaSidebarItemContent>
                      <VaImage :src="icons.icon3" 
                        alt="Icon Climate Protection Communal" style="width:2rem;" />
                      <VaSidebarItemTitle>
                        {{ $t("sidebar.dash2_1") }}
                      </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                  </VaSidebarItem>
                  <VaSidebarItem @click="goto('/dash2_2')" tabindex="0" role="link"
                    style="padding: 0;margin-left:1rem;">
                    <VaSidebarItemContent>
                      <VaImage :src="icons.icon2" 
                        alt="Icon Climate Protection Private" style="width:2rem;" />
                      <VaSidebarItemTitle>
                        {{ $t("sidebar.dash2_2") }}
                      </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                  </VaSidebarItem>
                  <VaSidebarItem @click="goto('/dash2_3')" tabindex="0" role="link"
                    style="padding: 0;margin-left:1rem;">
                    <VaSidebarItemContent>
                      <VaImage :src="icons.icon4"
                        alt="Icon CO2 Emissions" style="width:2rem;" />
                      <VaSidebarItemTitle>
                        {{ $t("sidebar.dash2_3") }}
                      </VaSidebarItemTitle>
                    </VaSidebarItemContent>
                  </VaSidebarItem>
                </template>
              </VaCollapse>
            </VaAccordion>
          </VaSidebarItemContent>
        </VaSidebarItem>

        <VaSidebarItem @click="goto('/dash3')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaImage :src="icons.icon5"
              alt="Icon Climate Adaptation" style="width:2rem;" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.dash3") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>

        <VaSidebarItem @click="goto('/test')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="info" size="2rem" />
            <VaSidebarItemTitle>
              Testseite
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>


        <VaSidebarItem @click="goto('/imprint')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="info" size="2rem" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.imprint") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem @click="goto('/gdpr')" tabindex="0" role="link">
          <VaSidebarItemContent>
            <VaIcon class="material-icons-outlined" name="privacy_tip" size="2rem" />
            <VaSidebarItemTitle>
              {{ $t("sidebar.gdpr") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
      </VaSidebar>
    </template>


    <template #content>
      <main class="p-4" id="main">

        <!-- use noto color emoji like so -->
        <!--
        <va-icon class="emoji"> &#x1F600; Click me! &#x1F389;</va-icon>
        -->

      <h2 class="prototype"> {{ $t("prototype") }}</h2>

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

.emoji {
  font-family: 'Noto Color Emoji';
  font-size: 1.5rem !important;
  font-weight: 400;
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

/* need vdeep to override vuestic styles */
.sidebar :deep(.va-collapse__header) {
  display: none;
}

.sidebar :deep(.va-collapse__header-wrapper) {
  display: none;
}

.sidebar :deep(.va-collapse__body-wrapper) {
  overflow-x: hidden;
}

.prototype {
  color: #ff0000;
  background-color: #ff0;
  font-size: 120%;
  padding:.3rem;
}

</style>

<style>

.headline {
  font-size: 2rem;
  font-weight: 500;
}

.headline.left {
  margin: 0;
  padding: 0;
  width: 10rem;
  text-align: left
}

.headline.right {
  margin: 0;
  padding: 0;
  width: 10rem;
  text-align: right;
}
</style>
