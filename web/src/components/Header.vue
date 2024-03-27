<template lang="pug">
v-btn(@click="goHomePage"
  class=["logo-btn"])
  v-icon(icon="mdi-home" 
    class=["mr-1"] color="#FFFFFF")
  p BBM

v-btn(style={fontWeight: 'bold', width: '20px', whiteSpace: 'nowrap'}
  rounded="xl" 
  size="x-large" 
  variant="flat" 
  class=["text-primary ml-auto"]
  density="compact") Hana
</template>
  
<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router'
export default defineComponent({
  name: 'Header',
  setup(){
    const router = useRouter()
    const goHomePage = () => {
            router.push('/')
        }
    return{
      goHomePage
    }
  }
})
</script>
  
<style scoped lang="sass">
  .logo-btn 
    font-size: 20px
    font-weight: bold
    white-space: nowrap
    width: fit-content

  </style>