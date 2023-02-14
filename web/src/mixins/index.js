export default {
  methods: {
    shuffle(array) {
      let currentIndex = array.length;
      let randomIndex;
      while (currentIndex !== 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
        [array[currentIndex], array[randomIndex]] = [
          array[randomIndex],
          array[currentIndex],
        ];
      }
      return array;
    },
    rsplit(x, delimiter, maxsplit) {
      x = x.split(delimiter || /s+/);
      if (x.length - 1 > maxsplit) {
        x = x.slice(0, -maxsplit).join(delimiter);
        x = [x].concat(x.slice(-maxsplit));
      }
      return x;
    },
    isEqual(x, y) {
      return JSON.stringify(x) === JSON.stringify(y);
    },
    isArray(obj) {
      return !!obj && obj.constructor === Array;
    },
    keyInObj(key, obj) {
      if (typeof obj !== 'object') return false;
      return Object.prototype.hasOwnProperty.call(obj, key);
    },
    endsWith(str, suffixes) {
      return suffixes.some((suffix) => str.endsWith(suffix));
    },
    capitalize(str) {
      return str && `${str.charAt(0).toUpperCase()}${str.slice(1)}`;
    },
  },
};
