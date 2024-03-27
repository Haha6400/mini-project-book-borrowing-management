<template lang="pug">
v-card
  v-layout
    v-navigation-drawer(color="#FFFFFF" permanent)
      v-dialog(max-width="60%", v-model="dialog_new_record" style={fontFamily: 'Poppins'})
        v-card
        EditRecord(title_record = "New Record", 
                        :closeDialog = "closeNewRecord"
                        :save = "save",
                        :item = "item")
            v-list( class=['text-primary'] style={width: '250px', fontSize:'20px'})
      template(v-slot:prepend) 
        v-btn(class=["text-none font-weight-bolder ma-6"]
          text="New Record"
          variant="flat" 
          color="primary"
          v-bind="activatorProps"
          size="x-large" 
          prepend-icon="mdi-plus"
          style={whiteSpace: 'nowrap'}
          rounded="lg"
          @click="newRecord"
          )

        v-list( class=['text-primary'] style={width: '250px', fontSize:'20px'})

          v-divider(:thickness="2" class=['border-opacity-75'] color="primary")

          v-list-item(prepend-icon="mdi-view-dashboard" link title="Dashboard")

          v-divider(:thickness="2" class=['border-opacity-75'] color="primary")

          v-list-group(value="Setting")
            template(v-slot:activator="{ props }" ) 
              v-list-item(v-bind="props" prepend-icon="mdi-cog" title="Setting")

            v-list-item(v-for="([title, icon], i) in setting" :key="i" :title="title" :prepend-icon="icon" :value="title")

    v-main(style="height: 868px")
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import EditRecord from "../components/EditRecord.vue";
import axios from 'axios'
export default defineComponent({
  name: 'SideBar',
  components: {
    EditRecord
  },
  setup() {
    
    // const items = ref([])
    const router = useRouter()
    

    const dialog_new_record = ref(false)

    const setting = [
      ['History', 'mdi-history'],
      ['Account', 'mdi-account-cog']
    ]
    const item = reactive({
      borrower_id: '',
      borrower_name: '',
      borrow_date: '',
      return_date: '',
      book_list: [{
        name: '',
        id: ''
      }],
      deposit: '',
    });

    onMounted(() => {
            // axios.get("http://localhost:8000/records")
            // .then((res) => {
            //     items.value = res.data;
            // }).catch((e) => {
            //     console.error(e)
            // })
        })

    const goHomePage = () => {
      router.push('/');
    };

    const newRecord = async () => {
      dialog_new_record.value = true;
    };

    const closeNewRecord = () => {
      dialog_new_record.value = false;
    };

    const save = async () => {
      closeNewRecord();
    };
    return {
      dialog_new_record,
      setting,
      item,
      goHomePage,
      newRecord,
      closeNewRecord,
      save,
    };
  },
})
</script>

<style scoped lang="sass">
.no-uppercase 
  text-transform: unset !important
.text-center 
  display: flex
  align-items: center
  justify-content: center

.pa-custom
  padding: 10px

.card-custom
  variant: "elevated"
  padding: 10px 10px 10px 10px
.v-card-title
  font-size: 25px
  font-weight: 500
  padding: 15px
  margin-left: 5px
</style>