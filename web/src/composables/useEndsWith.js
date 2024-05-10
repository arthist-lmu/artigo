export default function useEndsWith(str, suffixes) {
  return suffixes.some((suffix) => str.endsWith(suffix))
}
