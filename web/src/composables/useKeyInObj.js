export default function useKeyInObj(key, obj) {
  return !obj || typeof obj !== 'object' ? false : Object.hasOwnProperty.call(obj, key)
}
