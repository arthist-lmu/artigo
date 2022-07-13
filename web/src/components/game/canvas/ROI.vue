<template>
  <Canvas
    v-bind="$props"
    v-on="$listeners"
    @update="onUpdate"
  >
    <template v-slot:prepend-item>
      <v-row
        class="absolute mx-0 my-4"
        justify="center"
      >
        <v-col cols="auto">
          <v-slide-group
            v-model="tag"
            show-arrows
            mandatory
          >
            <v-slide-item
              v-for="tag in tags"
              :key="tag.name"
              v-slot="{ active, toggle }"
            >
              <v-chip
                @click="toggle"
                :color="active ? 'primary' : 'grey lighten-4'"
                class="mx-1"
                depressed
                rounded
              >
                {{ tag.name }}
              </v-chip>
            </v-slide-item>
          </v-slide-group>
        </v-col>
      </v-row>
    </template>
  </Canvas>
</template>

<script>
import Canvas from '@/components/game/canvas/Default.vue';

export default {
  extends: Canvas,
  props: {
    ...Canvas.props,
  },
  data() {
    return {
      tag: 0,
    };
  },
  methods: {
    onUpdate(values) {
      const { name } = this.tags[this.tag];
      const params = {
        tag: { name, ...values },
        language: this.$i18n.locale,
        resource_id: this.entry.resource_id,
      };
      this.$store.dispatch('game/post', params);
    },
    onKeyDown({ key }) {
      if (['ArrowLeft', 'a'].includes(key)) {
        if (this.tag > 0) {
          this.tag -= 1;
        }
      }
      if (['ArrowRight', 'd'].includes(key)) {
        if (this.tag + 1 < this.tags.length) {
          this.tag += 1;
        }
      }
    },
  },
  computed: {
    tags() {
      return this.entry.input_tags || [];
    },
  },
  watch: {
    tags: {
      handler(values) {
        if (values.length === 0) {
          this.$emit('error');
        }
      },
    },
  },
  created() {
    window.addEventListener('keydown', this.onKeyDown);
    this.tag = 0;
  },
  destroyed() {
    window.removeEventListener('keydown', this.onKeyDown);
  },
  components: {
    Canvas,
  },
};
</script>

<style scoped>
.row.absolute {
  position: absolute;
  width: 100%;
  z-index: 99;
}
</style>
