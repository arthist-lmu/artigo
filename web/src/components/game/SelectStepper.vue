<template>
  <v-stepper
    v-model="stepper"
    class="pb-0"
    vertical
    flat
  >
    <div
      v-for="(name, i) in Object.keys(params)"
      :key="name"
    >
      <v-stepper-step
        edit-icon="mdi-check"
        :complete="stepper > getStep(i)"
        :step="getStep(i)"
        editable
      >
        {{ $t('game.params')[name].title }}

        <small class="mt-1">
          <span v-if="typeof params[name].default === 'string'">
            {{ $t(`game.params.${name}.fields.${params[name].default}`) }}
          </span>

          <span v-if="typeof params[name].default === 'number'">
            {{ $tc(`game.params.${name}.suffix`, params[name].default) }}
          </span>
        </small>
      </v-stepper-step>

      <v-stepper-content
        :step="getStep(i)"
        :class="stepper === getStep(i) ? 'active' : undefined"
      >
        <v-select
          v-if="typeof params[name].default === 'string'"
          v-model="params[name].default"
          :items="params[name].items"
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

        <v-slider
          v-if="typeof params[name].default === 'number'"
          v-model="params[name].default"
          :min="params[name].min"
          :max="params[name].max"
          :step="params[name].step"
          append-icon="mdi-chevron-right"
          prepend-icon="mdi-chevron-left"
          hide-details
          dense
        />
      </v-stepper-content>
    </div>

    <template v-if="showMore">
      <div
        v-for="(config, i) in configs"
        :key="config.name"
      >
        <v-stepper-step
          :class="items[config.name].length > 1 ? undefined : 'disabled'"
          edit-icon="mdi-check"
          complete-icon="mdi-check"
          :complete="stepper > getStep(i, isPlugin = true)"
          :step="getStep(i, isPlugin = true)"
          :editable="items[config.name].length > 1"
        >
          {{ $t(`game.plugins.${config.name}.title`) }}

          <small class="mt-1">
            {{ $t(`game.plugins.${config.name}.fields.${data[config.name]}`) }}
          </small>
        </v-stepper-step>

        <v-stepper-content :step="getStep(i, isPlugin = true)">
          <v-select
            v-model="data[config.name]"
            :items="items[config.name]"
            item-value="name"
            class="mt-1"
            hide-details
            single-line
            outlined
            rounded
            dense
          >
            <template v-slot:item="{ item }">
              {{ $t(`game.plugins.${config.name}.fields.${item.name}`) }}
            </template>

            <template v-slot:selection="{ item }">
              {{ $t(`game.plugins.${config.name}.fields.${item.name}`) }}
            </template>
          </v-select>
        </v-stepper-content>
      </div>
    </template>
  </v-stepper>
</template>

<script>
import configs from '/config.json';

export default {
  props: {
    showMore: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      plugins: {
        resources: {
          icon: 'mdi-image-text',
          multiple: false,
        },
        opponents: {
          icon: 'mdi-account-outline',
          multiple: false,
        },
        inputs: {
          icon: 'mdi-tag-outline',
          multiple: false,
          setDefault: true,
        },
        taboos: {
          icon: 'mdi-tag-off-outline',
          multiple: false,
          setDefault: true,
        },
        suggesters: {
          icon: 'mdi-tag-check-outline',
          multiple: true,
          setDefault: true,
        },
      },
      params: {
        game_type: {
          icon: 'mdi-gamepad-outline',
          default: 'tagging',
          items: [],
        },
        resource_rounds: {
          icon: 'mdi-sort-numeric-variant',
          default: 5,
          min: 1,
          max: 25,
          step: 1,
        },
        game_round_duration: {
          icon: 'mdi-alarm',
          default: 60,
          min: 10,
          max: 60 * 60,
          step: 10,
        },
      },
      configs: [],
      stepper: 1,
      data: {},
    };
  },
  methods: {
    update() {
      const values = {
        score_type: [
          'annotation_validated_score',
          'opponent_validated_score',
        ],
        // TODO: move to config
        resource_min_roi_tags: 0,
        language: this.$i18n.locale,
      };
      Object.keys(this.params).forEach((name) => {
        values[name] = this.params[name].default;
      });
      Object.keys(this.data).forEach((name) => {
        if (!this.data[name].startsWith('no_')) {
          const pluginType = `${name.slice(0, -1)}_type`;
          values[pluginType] = this.data[name];
        }
      });
      this.$emit('input', values);
    },
    getStep(i, isPlugin = false) {
      if (isPlugin) {
        return i + 1 + Object.keys(this.params).length;
      }
      return i + 1;
    },
  },
  computed: {
    items() {
      const items = {};
      const game_type = this.params.game_type.default;
      this.configs.forEach(({ name, plugins }) => {
        if (this.plugins[name].setDefault) {
          items[name] = [{
            name: `no_${name}`,
            default: true,
          }];
        }
        plugins.forEach((plugin) => {
          if (plugin.game_types.includes(game_type)) {
            if (this.keyInObj(name, items)) {
              items[name].push(plugin);
            } else {
              items[name] = [plugin];
            }
          }
        });
      });
      return items;
    },
  },
  watch: {
    items: {
      handler(values) {
        this.data = {};
        Object.keys(values).forEach((name) => {
          values[name].forEach((plugin) => {
            if (plugin.default) {
              this.$set(this.data, name, plugin.name);
            }
          });
        });
      },
      deep: true,
    },
    params: {
      handler() {
        this.update();
      },
      deep: true,
    },
    data: {
      handler() {
        this.update();
      },
      deep: true,
    },
  },
  created() {
    this.configs = [];
    const values = new Set();
    Object.keys(configs).forEach((name) => {
      if (this.keyInObj(name, this.$t('game.plugins'))) {
        this.configs.push({
          name,
          plugins: configs[name],
        });
        configs[name].forEach(({ game_types }) => {
          game_types.forEach((value) => {
            values.add(value);
          });
        });
      }
    });
    this.params.game_type.items = Array.from(values);
  },
};
</script>
