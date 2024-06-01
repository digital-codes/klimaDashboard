<script setup>
import HelloWorld from './components/HelloWorld.vue'
import SizeAnimation from "./components/SizeAnimation.vue"

import { ref } from 'vue';
import { useBreakpoint } from 'vuestic-ui';

const showSidebar = ref(false)

const breakpoints = useBreakpoint()

const switchValue = ref(false)
</script>


<template>
  <VaLayout 
    style="height: 500px"
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
        <SizeAnimation></SizeAnimation>
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
