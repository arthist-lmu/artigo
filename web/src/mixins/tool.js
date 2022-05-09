import paper from 'paper';

export default {
  model: {
    prop: 'selected',
    event: 'update',
  },
  props: {
    selected: {
      type: String,
      required: true,
    },
    bounds: {
      required: true,
    },
  },
  data() {
    return {
      roi: null,
      tool: null,
      enabled: false,
      color: {
        fill: 'rgba(184, 201, 225, 1.0)',
        stroke: 'rgba(184, 201, 225, 0.5)',
      },
    };
  },
  methods: {
    onMouseDown() {

    },
    onMouseDraw() {

    },
    onMouseUp() {

    },
    set({
      x, y, width, height,
    }, relative = true) {
      if (width == null) {
        width = 0;
      }
      if (height == null) {
        height = 0;
      }
      if (relative) {
        const {
          xMin, width: imgWidth,
          yMin, height: imgHeight,
        } = this.bounds;
        x = (x - xMin) / imgWidth;
        y = (y - yMin) / imgHeight;
        width /= imgWidth;
        height /= imgHeight;
      }
      this.roi = {
        x, y, width, height,
      };
    },
    remove() {
      if (this.path) {
        this.path.removeSegments();
      }
    },
    update() {
      if (!this.isDisabled) {
        this.$emit('update', this.name);
      }
    },
  },
  computed: {
    isActive() {
      return this.selected === this.name;
    },
    isDisabled() {
      return false;
    },
  },
  watch: {
    isActive(active) {
      if (active) {
        this.tool.activate();
      }
    },
    isDisabled(disabled) {
      if (disabled && this.isActive) {
        this.$emit('update', null);
      }
    },
  },
  created() {
    this.tool = new paper.Tool({
      minDistance: 10,
      maxDistance: 45,
    });
    this.tool.onMouseDown = this.onMouseDown;
    this.tool.onMouseDrag = this.onMouseDrag;
    this.tool.onMouseUp = this.onMouseUp;
    if (this.isActive) {
      this.tool.activate();
    }
  },
};
