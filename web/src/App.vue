<template lang="pug">
v-app(style={fontSize: '20px', fontFamily: 'Poppins'})
  v-app-bar(app color="#8C2131")
    Header(:key="$route.fullPath")

  <!-- Sidebar -->
  v-navigation-drawer(app v-model="drawer" permanent)
    SideBar

  <!-- Main content -->
  v-main
    v-container(style={maxWidth: '100%', margin:0})
      router-view
</template>


<script>
import { defineComponent, ref } from 'vue'
import axios from "axios";
import Header from "./components/Header.vue";
import SideBar from "./components/SideBar.vue";
import Statistics from "./components/Statistics.vue";
import { useProvideCounterStore } from './store'

export default defineComponent({
  name: 'App',
  components: {
    Header,
    SideBar,
    Statistics
  },
  setup() {
    const drawer = ref(true);
    useProvideCounterStore()

    return {
      drawer,
    };
  },
});
</script>

<style scoped lang="sass">
</style>