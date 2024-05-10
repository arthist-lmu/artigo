<template>
  <v-container class="text-center fill-height">
    <v-row align="center">
      <v-col class="pa-0">
        <div :class="[mdAndDown ? 'text-h3' : 'text-h2', 'mb-4']">
          {{ $t('notFound.title') }}
        </div>

        <p class="mx-8 mb-4">
          {{ $t('notFound.fields.notExist') }}
        </p>

        <v-btn
          border="secondary md opacity-100"
          color="secondary"
          variant="outlined"
          rounded
          @click="goTo('home')"
        >
          <span class="text-primary-darken-1">
            {{ $t('notFound.fields.goHome') }}
          </span>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useDisplay } from 'vuetify'
import goTo from '@/composables/useGoTo'

const { mdAndDown } = useDisplay()
</script>
