import crypto from 'crypto';

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
    getHash(x) {
      const md5 = crypto.createHash('md5');
      return md5.update(JSON.stringify(x)).digest('hex');
    },
    getHeight(selector, padding = true) {
      const main = document.querySelector(selector);
      if (padding) return main.clientHeight;
      let { paddingTop, paddingBottom } = getComputedStyle(main);
      paddingTop = parseFloat(paddingTop);
      paddingBottom = parseFloat(paddingBottom);
      return main.clientHeight - paddingTop - paddingBottom;
    },
  },
};
