<template>
  <v-app :theme="darkMode ? 'dark' : 'light'">
    <v-layout>
      <v-main>
        <v-container class="fill-height">
          <v-row justify="center">
            <v-col :cols="$slots.default ? 6 : 'auto'">
              <v-container class="fill-height">
                <v-row
                  align="center"
                  no-gutters
                >
                  <LogoTemplate />
                </v-row>
              </v-container>
            </v-col>

            <v-col
              v-if="$slots.default"
              cols="6"
            >
              <slot />
            </v-col>
          </v-row>
        </v-container>
      </v-main>

      <FooterBar v-if="$slots.default" />
    </v-layout>

    <LoaderTemplate />
    <ToasterBar />
  </v-app>
</template>

<script setup>
import FooterBar from '@/components/FooterBar.vue'
import ToasterBar from '@/components/ToasterBar.vue'
import LogoTemplate from '@/components/LogoTemplate.vue'
import LoaderTemplate from '@/components/LoaderTemplate.vue'

defineProps({
  darkMode: {
    type: Boolean,
    default: false
  }
})
</script>
