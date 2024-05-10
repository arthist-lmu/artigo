export default function useIsArray(obj) {
  return !!obj && obj.constructor === Array
}
