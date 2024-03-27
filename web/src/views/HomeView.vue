<template lang="pug">
Statistics
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Statistics from "../components/Statistics.vue";


export default defineComponent({
    name: 'HomeView',
    components: {
        Statistics,
    },
    setup() {
        const drawer = ref(true);
        

        return {
            drawer
        }
        
    }
});
</script>

<style scoped lang="sass">

</style>