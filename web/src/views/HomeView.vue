<template>
  <v-container :key="locale">
    <v-row />

    <v-row
      v-if="statisticsData.creators && homeData"
      style="flex: 0;"
    >
      <v-col
        :class="mdAndDown ? 'px-4 py-6' : 'pa-12'"
        :cols="mdAndDown ? 12 : 10"
      >
        <div :class="textSize">
          <TyperTemplate
            :strings="[$t('home.texts.intro')]"
            :loop="false"
            @on-complete="show('creator')"
          />

          <transition
            name="fade"
            mode="out-in"
            appear
          >
            <span
              v-if="typer.creator && selectedCreator"
              :key="selectedCreator"
              class="space"
            >
              {{ selectedCreator }}.
            </span>
          </transition>

          <TyperTemplate
            v-if="typer.prefix"
            class="space"
            :strings="[$t('home.texts.prefix')]"
            :loop="false"
            @on-complete="show('examples')"
          />

          <TyperTemplate
            v-if="typer.examples"
            class="space"
            :remove-backspace="false"
            :strings="examples"
            :loop="false"
            @on-complete="show('button')"
          />
        </div>
      </v-col>
    </v-row>

    <transition
      name="fade"
      appear
    >
      <v-row
        v-if="typer.button"
        style="flex: 0;"
      >
        <v-col
          :class="[mdAndDown ? 'px-4 pb-6' : 'px-12 pb-12', 'pt-0']"
          :cols="mdAndDown ? 12 : 10"
        >
          <v-btn
            border="secondary md opacity-100"
            variant="outlined"
            size="x-large"
            rounded
            @click="goTo('game')"
          >
            {{ $t("home.fields.tryOut") }}
          </v-btn>

          <v-btn
            :title="$t('about.title')"
            class="ml-2"
            size="x-large"
            density="comfortable"
            icon="mdi-help-circle-outline"
            flat
            @click="goTo('about')"
          />

          <v-chip
            v-if="!mdAndDown"
            class="ml-10"
            variant="text"
            size="x-large"
          >
            <small style="font-size: 12px;">European Union Prize <br>for Citizen Science</small>

            <img
              height="100%"
              class="ml-6"
              src="/assets/images/eu-citizen-science-prize-logo.png"
              alt="European Union Prize for Citizen Science Logo"
            >
          </v-chip>
        </v-col>
      </v-row>
    </transition>

    <v-dialog
      v-model="showDialog"
      max-width="400"
    >
      <HelperCard
        :text="$t('language.helper')"
        icon="mdi-account-circle-outline"
        @close="showDialog = false;"
      />
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, nextTick, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import { useI18n } from 'vue-i18n'
import i18n from '@/plugins/i18n'
import shuffle from '@/composables/useShuffle'
import HelperCard from '@/components/HelperCard.vue'
import TyperTemplate from '@/components/TyperTemplate.vue'

const route = useRoute()
const router = useRouter()
const store = useStore()
const { t } = useI18n()
const { locale } = i18n.global
const { name, mdAndDown } = useDisplay()

const homeData = computed(() => store.state.home.data)
function goTo(name) {
  if (name === 'game') {
    if (!mdAndDown) {
      let params = {}
      homeData.value.forEach((entry) => {
        if (entry.type === 'annotated-creator') {
          params = { ...params, ...entry.params }
        }
      })
      store.commit('game/updateDialog', { params })
    }
  }
  router.push({ name })
}

const typer = ref({
  creator: false,
  prefix: false,
  examples: false,
  button: true
})
function show(name) {
  setTimeout(() => {
    nextTick(() => {
      if (route.name === 'home') {
        typer.value[name] = true
        window.scrollTo(0, document.body.scrollHeight)
      }
    })
  }, 250)
}
const selectedCreator = ref(null)
const statisticsData = computed(() => store.state.statistics.data)
watch(typer, ({ creator, prefix }) => {
  if (creator && !prefix) {
    let { names } = statisticsData.value.creators
    names = shuffle(names).slice(0, 4)
    homeData.value.forEach((entry) => {
      if (entry.type === 'annotated-creator') {
        names.push(entry.query)
      }
    })
    selectedCreator.value = names.shift()
    const timer = setInterval(() => {
      if (names.length === 0) {
        clearInterval(timer)
        show('prefix')
      } else {
        selectedCreator.value = names.shift()
      }
    }, 1000)
  }
}, { deep: true })
watch(locale, () => {
  typer.value = {
    creator: false,
    prefix: false,
    examples: false,
    button: true
  }
})

const textSize = computed(() => {
  const values = ['accent--text']
  switch (name) {
    case 'xs':
      values.push('text-h4')
      break
    case 'sm':
      values.push('text-h3')
      break
    default:
      values.push('text-h2')
      break
  }
  return values
})

const examples = computed(() => {
  return [
    t('home.texts.example1'),
    t('home.texts.example2'),
    t('home.texts.example3'),
    t('home.texts.example4'),
    t('home.texts.example5'),
    t('home.texts.example1')
  ]
})

onMounted(() => {
  // see: @/components/game/Drawer.vue
  // store.dispatch('statistics/get')
  window.scrollTo(0, document.body.scrollHeight)
})

const showDialog = ref(false)
if (localStorage.getItem('langHelper') === null) {
  localStorage.setItem('langHelper', true)
  showDialog.value = true
}
</script>

<style scoped>
.v-container {
  flex-direction: column;
  display: flex;
  height: 100%;
}

.text-h2 {
  line-height: 4.75rem;
}

.text-h2 .v-icon {
  font-size: 60px;
}

.text-h3 {
  line-height: 3.75rem;
}

.text-h3 .v-icon {
  font-size: 48px;
}

.text-h4 {
  line-height: 2.75rem;
}

.text-h4 .v-icon {
  font-size: 34px;
}

span.space::before {
  content: " ";
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .5s
}

.fade-enter,
.fade-leave-to {
  opacity: 0
}
</style>
