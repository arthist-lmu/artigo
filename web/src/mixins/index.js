export default {
  methods: {
    keyInObj(key, obj) {
      if (typeof obj !== 'object') return false;
      return Object.prototype.hasOwnProperty.call(obj, key);
    },
    isEqual(x, y) {
      return JSON.stringify(x) === JSON.stringify(y);
    },
    isArray(obj) {
      return !!obj && obj.constructor === Array;
    },
    capitalize(str) {
      return str && `${str.charAt(0).toUpperCase()}${str.slice(1)}`;
    },
  },
};
