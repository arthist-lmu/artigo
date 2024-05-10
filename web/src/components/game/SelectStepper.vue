<template>
  <v-stepper
    v-model="stepper"
    style="display: none;"
  />

  <v-stepper
    v-model="stepper"
    non-linear
    flat
  >
    <template
      v-for="(name, i) in Object.keys(data)"
      :key="name"
    >
      <v-stepper-header v-if="i < 3 || showMore">
        <v-stepper-item
          :complete="stepper > i"
          :step="i"
          :value="i"
          :disabled="data[name].default === undefined"
          :editable="data[name].default !== undefined"
        >
          <template #icon="{ hasCompleted, step }">
            <v-btn
              v-if="hasCompleted"
              class="bg-primary"
              icon="mdi-check"
            />
            <v-avatar
              v-else
              color="primary"
            >
              {{ step + 1 }}
            </v-avatar>
          </template>

          <template #title>
            {{ $t(`game.params.${name}.title`) }}
          </template>

          <template #subtitle>
            <div
              v-if="data[name].default !== undefined"
              class="mt-2"
            >
              <template v-if="typeof data[name].default === 'string'">
                {{ $t(`game.params.${name}.fields.${data[name].default}`) }}
              </template>

              <template v-if="typeof data[name].default === 'number'">
                {{ $t(`game.params.${name}.suffix`, data[name].default) }}
              </template>
            </div>
          </template>
        </v-stepper-item>
      </v-stepper-header>

      <v-stepper-window
        v-show="stepper == i"
        direction="vertical"
      >
        <v-stepper-window-item :value="i">
          <template v-if="typeof data[name].default === 'string'">
            <v-select
              v-model="data[name].default"
              :items="data[name].items"
              border="md"
              variant="outlined"
              density="compact"
              hide-details
              single-line
              rounded
            >
              <template #item="{ props: propsSelect, item }">
                <v-list-item
                  v-bind="propsSelect"
                  :title="$t(`game.params.${name}.fields.${item.raw}`)"
                />
              </template>

              <template #selection="{ item }">
                {{ $t(`game.params.${name}.fields.${item.raw}`) }}
              </template>
            </v-select>

            <v-combobox
              v-if="data[name].default.startsWith('custom_')"
              v-model="data[name].params[`${data[name].default.split('_')[1]}_inputs`]"
              :placeholder="$t(`game.inputs.${data[name].default}`)"
              class="mt-2"
              border="md"
              variant="outlined"
              density="compact"
              hide-details
              single-line
              multiple
              rounded
              chips
            >
              <template #selection="{ item }">
                <v-chip
                  class="mr-1 ml-0"
                  color="primary"
                  variant="outlined"
                  size="small"
                  close
                >
                  {{ item.raw }}
                </v-chip>
              </template>
            </v-combobox>
          </template>

          <v-slider
            v-if="typeof data[name].default === 'number'"
            v-model="data[name].default"
            :min="settings[name].min"
            :max="settings[name].max"
            :step="settings[name].step"
            append-icon="mdi-chevron-right"
            prepend-icon="mdi-chevron-left"
            thumb-size="10"
            track-size="2"
            color="primary"
            hide-details
          />
        </v-stepper-window-item>
      </v-stepper-window>
    </template>
  </v-stepper>
</template>

<script setup>
import { ref, watch } from 'vue'
import i18n from '@/plugins/i18n'
import isArray from '@/composables/useIsArray'
import keyInObj from '@/composables/useKeyInObj'
// eslint-disable-next-line
import defaultConfig from '/config.json'

const { locale } = i18n.global

const props = defineProps({
  defaultParams: {
    type: Object,
    default: null
  },
  showMore: {
    type: Boolean,
    default: false
  }
})

const data = ref({
  game_type: {
    default: null
  }
})
const stepper = ref(0)

const settings = ref({
  game_type: {
    default: 'tagging'
  },
  game_round_duration: {
    min: 20,
    max: 600,
    step: 20,
    default: 60
  },
  resource_rounds: {
    min: 1,
    max: 25,
    step: 1,
    default: 5
  },
  resource_type: {

  },
  opponent_type: {
    setNone: true
  },
  input_type: {

  },
  taboo_type: {

  },
  suggester_type: {
    multiple: true
  }
})

function setDefaultParams(params) {
  if (params) {
    Object.entries(params).forEach(([name, values]) => {
      if (keyInObj(name, data.value)) {
        data.value[name].default = values
      } else {
        const configName = name.split('_')[0]
        const pluginType = `${configName}_type`
        if (keyInObj(pluginType, data.value)) {
          if (!keyInObj('params', data.value[pluginType])) {
            data.value[pluginType].params = {}
          }
          if (isArray(values)) {
            data.value[pluginType].params[name] = []
            values.forEach((value, i) => {
              data.value[pluginType].params[name][i] = value
            })
          } else {
            data.value[pluginType].params[name] = values
          }
        }
      }
    })
  }
}

watch(() => data.value.game_type.default, (value) => setDefaultConfig(value))
const ensureObjectProperty = (obj, prop, defaultValue) => {
  if (!Object.prototype.hasOwnProperty.call(obj, prop)) {
    obj[prop] = defaultValue
  }
}
function setDefaultConfig(gameType) {
  const validPluginTypes = new Set()
  currentConfig.value.forEach(({ name: configName, plugins }) => {
    const pluginType = `${configName}_type`
    plugins.forEach((plugin) => {
      if (plugin.game_types.includes(gameType)) {
        validPluginTypes.add(pluginType)
        if (keyInObj(pluginType, settings.value)) {
          ensureObjectProperty(data.value, pluginType, {})
          ensureObjectProperty(data.value[pluginType], 'params', {})
          ensureObjectProperty(data.value[pluginType], 'items', [])
          data.value[pluginType].items.push(plugin.name)
          if (!keyInObj('default', data.value[pluginType]) && plugin.default) {
            data.value[pluginType].default = plugin.name
          }
          if (plugin.params) {
            Object.entries(plugin.params).forEach(([param, values]) => {
              const configParam = `${configName}_${param}`
              if (keyInObj(configParam, settings.value)) {
                if (!keyInObj(configParam, data.value)) {
                  data.value[configParam] = {}
                }
                if (!keyInObj('default', data.value[configParam])) {
                  data.value[configParam].default = values
                }
              } else if (!keyInObj(configParam, data.value[pluginType].params)) {
                data.value[pluginType].params[configParam] = values
              }
            })
          }
        }
      }
    })
    if (
      keyInObj(pluginType, data.value)
      && keyInObj('items', data.value[pluginType])
    ) {
      if (!keyInObj('default', data.value[pluginType])) {
        data.value[pluginType].default = `no_${configName}`
        data.value[pluginType].items.unshift(`no_${configName}`)
      } else if (settings.value[pluginType].setNone) {
        data.value[pluginType].items.unshift(`no_${configName}`)
      }
    }
  })
  Object.keys(data.value).forEach((pluginType) => {
    const isType = pluginType.split('_')[1] === 'type'
    const isNotGame = pluginType.split('_')[0] !== 'game'
    if (!validPluginTypes.has(pluginType) && isNotGame && isType) {
      delete data.value[pluginType]
    }
  })
}

watch(data, () => update(), { deep: true })
const emit = defineEmits(['update:modelValue'])
function update() {
  const input = {
    score_type: [
      'annotation_validated_score',
      'opponent_validated_score'
    ],
    game_language: locale.value
  }
  Object.entries(data.value).forEach(([pluginType, { default: defaultValue, params }]) => {
    if (defaultValue !== undefined) {
      input[pluginType] = defaultValue
    }
    if (params) {
      Object.entries(params).forEach(([param, values]) => {
        const isValid = typeof values === 'string' && values.length
          || typeof values === 'number'
          || (isArray(values) && values.length)
        if (!keyInObj(param, data) && isValid) {
          input[param] = values
        }
      })
    }
  })
  emit('update:modelValue', input)
}

const currentConfig = ref([])
const gameTypeItems = new Set()
Object.entries(defaultConfig).forEach(([configName, plugins]) => {
  currentConfig.value.push({
    name: configName,
    plugins
  })
  plugins.forEach(({ game_types }) => {
    game_types.forEach((gameType) => {
      gameTypeItems.add(gameType)
    })
  })
})
settings.value.game_type.items = [...gameTypeItems]
Object.entries(settings.value).forEach(([configParam, values]) => {
  const configData = data.value[configParam] = {}
  if (keyInObj('default', values)) {
    configData.default = values.default
  }
})
data.value.game_type.items = gameTypeItems
setDefaultParams(props.defaultParams)
</script>

<style>
.v-stepper-item > .v-avatar {
  margin-right: 24px !important;
}
</style>

<style scoped>
.v-stepper-header {
  box-shadow: none;
}

.v-stepper-item {
  text-align: left;
}

.v-stepper-item--disabled {
  opacity: 0.15;
}

.v-window {
  margin: 4px 0 4px 48px;
}
</style>
