<template lang="pug">
v-card(flat)
    v-card-title(class=["d-flex text-primary textWeight: 'bolder'"])
        v-row
            v-col(cols="6" sm="4" md="3")
                
                v-menu.w-100
                    template(v-slot:activator="{ props }")
                        v-text-field(
                            placeholder="YYYY-MM-DD"
                            label="From" 
                            v-model="from_search" 
                            variant="outlined" 
                            v-bind="props")
                    v-date-picker(@update:modelValue="onInputFrom" )
                
            
            v-col(cols="6" sm="4" md="3")
                v-menu.w-100
                    template(v-slot:activator="{ props }")
                        v-text-field(
                            placeholder="YYYY-MM-DD"
                            label="To" 
                            v-model="to_search" 
                            variant="outlined" 
                            v-bind="props")
                    v-date-picker(@update:modelValue="onInputTo")
            
        v-spacer

        v-responsive(class="mx-auto" max-width="400")
            v-text-field(v-model="search"
                placeholder="Search"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                hide-details="auto"
                )

v-card(color = "#FFFFFF" class=["w-full", "ma-2"])
    v-card-title(class=["d-flex align-center pe-2"] 
        style="{fontWeight: 'bolder'}") Book Borrowing Statistics
    v-spacer
    v-divider(:thickness="2" class=['border-opacity-75'] color="primary")
    v-data-table(:headers="headers" 
        :items="items_filter" 
        :items-per-page="items_per_page"
        item-key="id"
        v-model:page="page"
        v-model:sort-by="sortBy"
        :search="search"
        @update:model-value="items_per_page = parseInt($event, 10)")
        //- Delete banner
        template(v-slot:top)
            v-dialog(v-model="dialog_delete" max-width="500px")
                v-card(style="fontFamily:'Poppins'")
                    v-card-title(class=["text-center text-primary"]) Are you sure?
                    div(class=["text-center"]) This action cannot be undone.
                    div(class=["text-center"]) All values associated with this field will be lost
                    v-btn(variant="elevated" style="margin: 15px" full-width class=['button-custom'] rounded="lg" size="large" color="primary" @click="deleteItemConfirm") Delete
                    v-btn(variant="outlined" style="margin: 0px 15px 15px 15px" full-width  class=['button-custom']  rounded="lg" size="large" color="primary" @click="closeDelete") Cancel
                    v-spacer
            //- Update item
            v-dialog(v-model="dialog_update" max-width="60%")
                v-card(style="fontFamily:'Poppins'")
                    EditRecord(title_record = "Update Record", 
                        :closeDialog = "closeUpdate"
                        :save = "save",
                        :item = "updated_item")
            //View details order
            v-dialog(v-model="dialog_view" max-width="60%")
                v-card(style="fontFamily:'Poppins'")
                    EditRecord(title_record = "View Details", 
                        :closeDialog = "closeView"
                        :save = "save",
                        :item = "updated_item")
        template(v-slot:item.status="{ value }")
            v-chip(:color="getColor(value)" )
                | {{ value }}
        template(v-slot:item.action="{ item }")
            v-icon(size="small" class=["me-2"] @click="viewDetails(item)" color="orange")
                | mdi-dots-vertical
            v-icon(size="small" class=["me-2"] @click="updateItem(item)" color="blue")
                | mdi-square-edit-outline
            v-icon(size="small" @click="deleteItem(item)" color="primary")
                | mdi-trash-can-outline
        template(v-slot:bottom)
            div(class="text-center pt-2")
                v-pagination(v-model="page"
                    :length="page_count")
</template>

<script>
import { defineComponent, ref, computed, onMounted} from 'vue';

import EditRecord from "../components/EditRecord.vue";
import axios from 'axios';
import { useCounterStore } from '../store'

export default defineComponent({
    name: 'Statistics',
    components: {
        EditRecord,
    },
    setup() {
        const {items, getItemValue} = useCounterStore()

        const search = ref('')
        const from_search = ref(null);
        const to_search = ref(null);
        const dialog_view = ref(false)
        const dialog_delete = ref(false)
        const dialog_update = ref(false)
        const page = ref(1)
        const items_per_page = ref("10")
        const headers = ref([
            {
                title: 'ID',
                align: 'start',
                value: 'id',
                class: 'font-weight-bold ',
                key: 'id'
            },
            { title: 'Borrower', value: 'borrower', sortable: false },
            { title: 'Borrow Date', value: 'borrow_date', align: 'center', sortable: false, type: 'date' },
            { title: 'Return Date', value: 'return_date', align: 'center', sortable: false, type: 'date' },
            { title: 'Total Deposit (VND)', value: 'total_deposit', align: 'end', sortable: false, type: 'number' },
            { title: 'Status', value: 'status', align: 'center' },
            { title: 'Action', value: 'action', align: 'center', sortable: false }
        ])
        const sortBy = [{ key: 'id', order: 'asc' }]
        const index = ref(-1)
        const default_item = {
            id: '',
            borrower_id: '',
            borrower: '',
            borrow_date: '',
            return_date: '',
            book_list: [],
            total_deposit: '',
            status: ''
        }

        const updated_item = ref({
            id: '',
            borrower_id: '',
            borrower: '',
            borrow_date: '',
            return_date: '',
            book_list: [],
            total_deposit: '',
            status: ''
        })


        const getColor = (status) => {
            if (status == "BORROWING") return 'blue';
            else if (status == "OVERDUE") return 'orange';
            else if (status == "RETURNED") return 'green';
            else return 'red';
        };

        const viewDetails = (item) => {
            index.value = items.value.indexOf(item);
            updated_item.value = { ...item };
            axios.get(`http://localhost:8000/books/${updated_item.value.id}`)
                .then((response) => {
                    updated_item.value.book_list = response.data
                })
                .catch((error) => console.error(error))
            dialog_view.value = true;
        };

        const updateItem = async (item) => {
            index.value = items.value.indexOf(item);
            console.log("index.value", index.value)
            updated_item.value = { ...item };
            const response = await axios.get(`http://localhost:8000/books/${updated_item.value.id}`);
            updated_item.value.book_list = response.data;

            dialog_update.value = true;
        };

        const deleteItem = (item) => {
            index.value = items.value.indexOf(item);
            updated_item.value = { ...item };
            dialog_delete.value = true;
        };

        const deleteItemConfirm = () => {
            console.log(updated_item.value.id)
            axios.delete(`http://localhost:8000/record/${updated_item.value.id}`)
                .then((response) => {
                    console.log(response)
                    const indexItem = items.value.indexOf(updated_item);
                    items.value.splice(indexItem, 1);
                    getItemValue()
                    closeDelete();
                })
                .catch((error) => console.error(error))
            
        };

        const closeDelete = () => {
            dialog_delete.value = false;
            updated_item.value = { ...default_item };
            index.value = -1;
        };

        const closeView = () => {
            dialog_view.value = false;
            updated_item.value = { ...default_item };
            index.value = -1;
        };

        const closeUpdate = () => {

            dialog_update.value = false;
            updated_item.value = { ...default_item };
            index.value = -1;
        };


        const onInputFrom = (event) => {
            from_search.value = formatDate(event)
        };

        const onInputTo = (event) => {
            to_search.value = formatDate(event)
        };

        const formatDate = (event) =>{
            const date = new Date(event);
            const year = date.getFullYear();
            const month = ("0" + (date.getMonth() + 1)).slice(-2);
            const day = ("0" + date.getDate()).slice(-2);
            const formattedDate = `${year}-${month}-${day}`;
            return formattedDate;
        }

        const save = () => {
            if (index.value > -1) {
                Object.assign(items.value[index.value], updated_item.value);
            } else {
                items.value.splice(items.value.findIndex((item) => { return item.id === updated_item.value.id }), 1, updated_item.value)
            }
            console.log("closeeeee")
            closeUpdate();
        };

        const page_count = computed(() => {
            return Math.ceil(items.value.length / Number(items_per_page.value));
        });

        const items_filter = computed(() => {
            if(from_search.value && to_search.value) {
                console.log("true")
                console.log("from_search.value",from_search.value, "to_search.value", to_search.value)
                const fromDate = new Date(from_search.value);
                const toDate = new Date(to_search.value);
                getItemValue()
                items.value = items.value.filter(item => {
                    const itemBorrowDate = new Date(item.borrow_date);
                    const itemReturnDate = new Date(item.return_date);
                    return itemBorrowDate >= fromDate && itemReturnDate <= toDate;
                });
            }
            return items.value.map(item => ({
                    ...item,
                    borrower: `[${item.borrower_id}] ${item.borrowerName}`
                }));
        });

        onMounted(async () => {
            await getItemValue()
            
        });

        return {
            onInputFrom,
            onInputTo,
            formatDate,
            search,
            dialog_view,
            dialog_delete,
            dialog_update,
            page,
            items_per_page,
            default_item,
            updated_item,
            sortBy,
            index,
            headers,
            items,
            getColor,
            viewDetails,
            updateItem,
            deleteItem,
            deleteItemConfirm,
            closeDelete,
            closeView,
            closeUpdate,
            save,
            page_count,
            items_filter,
            from_search,
            to_search,
        };


    },
})
</script>

<style scoped lang="sass">
  .no-uppercase 
    text-transform: unset !important

.back-white
    color: #000000

.button-custom
    display: flex
    align-items: center
    justify-content: center
</style>