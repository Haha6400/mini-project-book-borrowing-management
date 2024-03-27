import { ref } from 'vue'
import { createInjectionState } from '@vueuse/core'
import axios from 'axios'; 
const [useProvideCounterStore, useCounterStore] = createInjectionState(() => {
  // state
  const items = ref([])
  const getItemValue = async  () => {
    const res =  await axios.get("http://localhost:8000/records");
    items.value = res.data   
    console.log("items.value", items.value[items.value.length -1])
  }
  return {items, getItemValue }
})
export { useProvideCounterStore }
export { useCounterStore }