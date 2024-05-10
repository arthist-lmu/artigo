export default function useCapitalize(str) {
  return str && `${str.charAt(0).toUpperCase()}${str.slice(1)}`
}
