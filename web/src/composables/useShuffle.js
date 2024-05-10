export default function useShuffle(array) {
  for (let currentIndex = array.length - 1; currentIndex > 0; currentIndex--) {
    const randomIndex = Math.floor(Math.random() * (currentIndex + 1))
    const element = array[currentIndex]
    array[currentIndex] = array[randomIndex]
    array[randomIndex] = element
  }
  return array
}
