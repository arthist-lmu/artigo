<template>
  <v-stepper
    v-model="stepper"
    class="pb-0"
    vertical
    flat
  >
    <div
      v-for="(name, i) in Object.keys(data)"
      :key="name"
      :class="{
        'border-left': (i < (3 - 1) && !showMore) || (i < Object.keys(data).length - 1 && showMore),
        active: stepper === i + 1
      }"
    >
      <template v-if="i < 3 || showMore">
        <v-stepper-step
          :class="{ disabled: data[name].default === undefined }"
          :complete="stepper > i + 1"
          :step="i + 1"
          :editable="data[name].default !== undefined"
          complete-icon="mdi-check"
          edit-icon="mdi-check"
        >
          {{ $t('game.params')[name].title }}

          <small class="mt-1">
            <span v-if="typeof data[name].default === 'string'">
              {{ $t(`game.params.${name}.fields.${data[name].default}`) }}
            </span>

            <span v-if="typeof data[name].default === 'number'">
              {{ $tc(`game.params.${name}.suffix`, data[name].default) }}
            </span>
          </small>
        </v-stepper-step>

        <v-stepper-content :step="i + 1">
          <template v-if="typeof data[name].default === 'string'">
            <v-select
              v-model="data[name].default"
              :items="data[name].items"
              class="mt-1"
              hide-details
              single-line
              outlined
              rounded
              dense
            >
              <template v-slot:item="{ item }">
                {{ $t(`game.params.${name}.fields.${item}`) }}
              </template>

              <template v-slot:selection="{ item }">
                {{ $t(`game.params.${name}.fields.${item}`) }}
              </template>
            </v-select>

            <v-combobox
              v-if="data[name].default.startsWith('custom_')"
              v-model="data[name].params[`${data[name].default.split('_')[1]}_inputs`]"
              :placeholder="$t(`game.inputs.${data[name].default}`)"
              class="mt-2"
              hide-details
              single-line
              outlined
              multiple
              rounded
              chips
              dense
            >
              <template v-slot:selection="{ item }">
                <v-chip
                  class="mr-1 ml-0"
                  color="primary"
                  outlined
                  dense
                  close
                  small
                >
                  {{ item }}
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
            hide-details
            dense
          />
        </v-stepper-content>
      </template>
    </div>
  </v-stepper>
</template>

<script>
// eslint-disable-next-line
import configs from '/config.json';

export default {
  props: {
    defaultParams: Object,
    showMore: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      settings: {
        game_type: {
          default: 'tagging',
        },
        game_round_duration: {
          min: 20,
          max: 600,
          step: 20,
          default: 60,
        },
        resource_rounds: {
          min: 1,
          max: 25,
          step: 1,
        },
        resource_type: {

        },
        opponent_type: {

        },
        input_type: {

        },
        taboo_type: {

        },
        suggester_type: {
          multiple: true,
        },
      },
      isSetup: false,
      configs: [],
      stepper: 1,
      data: {},
    };
  },
  methods: {
    update() {
      const input = {
        score_type: [
          'annotation_validated_score',
          'opponent_validated_score',
        ],
        language: this.$i18n.locale,
      };
      Object.entries(this.data).forEach(([pluginType, { default: defaultValue, params }]) => {
        if (defaultValue !== undefined) {
          input[pluginType] = defaultValue;
          if (params !== undefined) {
            Object.entries(params).forEach(([configParam, values]) => {
              if (!this.keyInObj(configParam, this.data)) {
                if (
                  (typeof values === 'string' && values.length)
                  || (typeof values === 'number')
                  || (this.isArray(values) && values.length)
                ) {
                  input[configParam] = values;
                }
              }
            });
          }
        }
      });
      this.$emit('input', input);
    },
    setDefault(params) {
      if (params && Object.keys(params).length) {
        Object.entries(params).forEach(([name, values]) => {
          if (this.keyInObj(name, this.data)) {
            this.$set(this.data[name], 'default', values);
          } else {
            const configName = name.split('_')[0];
            const pluginType = `${configName}_type`;
            if (this.keyInObj(pluginType, this.data)) {
              if (!this.keyInObj('params', this.data[pluginType])) {
                this.$set(this.data[pluginType], 'params', {});
              }
              if (this.isArray(values)) {
                this.$set(this.data[pluginType].params, name, []);
                values.forEach((value, i) => {
                  this.$set(this.data[pluginType].params[name], i, value);
                });
              } else {
                this.$set(this.data[pluginType].params, name, values);
              }
            }
          }
        });
      }
    },
  },
  watch: {
    data: {
      handler() {
        this.update();
      },
      deep: true,
    },
    defaultParams(values) {
      this.setDefault(values);
    },
    'data.game_type.default': {
      handler(gameType) {
        const validPluginTypes = new Set();
        this.configs.forEach(({ name: configName, plugins }) => {
          const pluginType = `${configName}_type`;
          plugins.forEach((plugin) => {
            if (plugin.game_types.includes(gameType)) {
              validPluginTypes.add(pluginType);
              if (this.keyInObj(pluginType, this.settings)) {
                if (!this.keyInObj(pluginType, this.data)) {
                  this.$set(this.data, pluginType, {});
                }
                if (!this.keyInObj('params', this.data[pluginType])) {
                  this.$set(this.data[pluginType], 'params', {});
                }
                if (!this.keyInObj('items', this.data[pluginType])) {
                  this.$set(this.data[pluginType], 'items', []);
                }
                this.data[pluginType].items.push(plugin.name);
                if (!this.keyInObj('default', this.data[pluginType]) && plugin.default) {
                  this.$set(this.data[pluginType], 'default', plugin.name);
                }
                if (plugin.params !== undefined) {
                  Object.entries(plugin.params).forEach(([param, values]) => {
                    const configParam = `${configName}_${param}`;
                    if (this.keyInObj(configParam, this.settings)) {
                      if (!this.keyInObj(configParam, this.data)) {
                        this.$set(this.data, configParam, {});
                      }
                      if (!this.keyInObj('default', this.data[configParam])) {
                        this.$set(this.data[configParam], 'default', values);
                      }
                    } else if (!this.keyInObj(configParam, this.data[pluginType].params)) {
                      this.$set(this.data[pluginType].params, configParam, values);
                    }
                  });
                }
              }
            }
          });
          if (
            this.keyInObj(pluginType, this.data)
            && this.keyInObj('items', this.data[pluginType])
            && !this.keyInObj('default', this.data[pluginType])
          ) {
            this.$set(this.data[pluginType], 'default', `no_${configName}`);
            this.data[pluginType].items.unshift(`no_${configName}`);
          }
        });
        Object.keys(this.data).forEach((pluginType) => {
          if (
            !validPluginTypes.has(pluginType)
            && pluginType.split('_')[0] !== 'game'
            && pluginType.split('_')[1] === 'type'
          ) {
            this.$delete(this.data, pluginType);
          }
        });
        if (!this.isSetup) {
          // set default params only on setup
          this.setDefault(this.defaultParams);
          this.isSetup = true;
        }
      },
    },
  },
  created() {
    this.configs = [];
    let gameItems = new Set();
    Object.keys(configs).forEach((configName) => {
      const plugins = configs[configName];
      this.configs.push({
        name: configName,
        plugins,
      });
      plugins.forEach(({ game_types }) => {
        game_types.forEach((value) => {
          gameItems.add(value);
        });
      });
    });
    gameItems = Array.from(gameItems);
    this.$set(this.settings.game_type, 'items', gameItems);
    Object.entries(this.settings).forEach(([configParam, values]) => {
      this.$set(this.data, configParam, {});
      if (this.keyInObj('default', values)) {
        this.$set(this.data[configParam], 'default', values.default);
      }
    });
    this.$set(this.data.game_type, 'items', gameItems);
  },
};
</script>
