<template lang="pug">
v-card
    v-card-title(class=["d-flex align-center pe-2"]) {{title_record}}
    v-divider(:thickness="2" class=['border-opacity-75'] color="primary")
v-card(class=["w-full card-custom"])
    v-space
    v-row(class = ["text-size-margin"]) 
        v-col(class=["w-full pa-custom-text"])
            v-col-title Borrower's Code*
            v-text-field(variant="outlined"  :rules="rules('borrower')" v-model="record.borrower_id" ) 
        v-col(class=["w-full pa-custom-text"])
            v-col-title Borrower's Name*
            v-text-field(variant="outlined"  disabled)  {{ borrower_name }}

    v-row(class = ["text-size-margin"]) 
        v-col(class=["w-full pa-custom-text"])
            v-col-title Borrower Date*
            v-text-field(type="date" variant="outlined" :rules="rules()" v-model="record.borrow_date")
        v-col(class=["w-full pa-custom-text"])
            v-col-title Return Date*
            v-text-field(type="date" variant="outlined" :rules="rules()" v-model= "record.return_date")
        v-col(v-if="title_record === 'Update Record' || title_record === 'New Record'" class=["w-full pa-custom-text"])
            v-col-title Total Deposit
            v-text-field.custom-disabled(variant="outlined" :disabled="true") {{total_deposit }}
        v-col(v-if="title_record === 'View Details'" class=["w-full pa-custom-text"])
            v-col-title Total Deposit
            v-text-field.custom-disabled(variant="outlined" :disabled="true" v-model="record.total_deposit")

        v-col(v-if="title_record === 'Update Record'" class=["w-full pa-custom-text"])
            v-col-title Status
            v-select(:items="['BORROWING', 'RETURNED', 'FAILED', 'OVERDUE']"
                item-title= "status"
                v-model="record.status"
                variant="outlined"
                persistent-hint
                return-object
                single-line)
        v-col(v-if="title_record === 'View Details'" class=["w-full pa-custom-text"])
            v-col-title Status
            v-text-field(variant="outlined" v-model= "record.status")
        v-col(v-if="title_record !== 'New Record'" class=["w-full pa-custom-text"])
            v-col-title Fee
            v-text-field(variant="outlined" :disabled="true") {{ calculateFee }}
    v-divider(:thickness="2" class=['border-opacity-75'] color="primary")


    v-row(class = ["text-size-margin"] )
        v-col(class=["pa-custom-text"] cols="4" sm="3" md="2")
            v-col-title Book Code*
        v-col(class=["pa-custom-text"])
            v-col-title Book Name*
        v-col(class=["pa-custom-text"] cols="4" sm="3" md="3")
            v-col-title  Deposit (VND)*
        

    v-row( v-for="(item, index) in record.book_list" :id="index" class = ["text-size-margin"])
        v-col(class=["pa-custom-field"] cols="4" sm="3" md="2")
            v-text-field(variant="outlined" v-model="item.id" :rules="rules('book')" @input="updateNameDeposit(item)")
        v-col(class=["pa-custom-field"])
            v-text-field(variant="outlined" :disabled="true" ) {{ item.name }}
        v-col(class=["pa-custom-field"] cols="4" sm="3" md="3")
            v-text-field(variant="outlined" type="number" :disabled="true") {{ item.deposit }}
            
        v-col(v-if="title_record === 'Update Record' || title_record === 'New Record'" cols="1" sm="1" md="1" class=["pa-0"])
            v-btn(icon="mdi-trash-can-outline" variant="elevated" block rounded="lg"  size="large"  color="primary" @click="deleteItem(index)")

    v-row(v-if="title_record === 'Update Record' || title_record === 'New Record'" style={margin: '0'})
        v-col(class=["pa-0"])
            v-btn(style={fontSize:'14px', fontFamily: 'Poppins'} prepend-icon="mdi-plus" variant="text"  @click="addItem" class=["no-uppercase"]) Add more books...


    v-row(class = ["text-size-margin"]) 
        v-col(class=["w-full pa-custom-text"])
            v-col-title(style={fontSize:'18px'}) Note
            v-textarea(variant="outlined" row-height="15" rows="1" auto-grow v-model="record.note")

    v-row(v-if="title_record === 'Update Record' || title_record === 'New Record'" class = ["text-size-margin"]) 
        v-col(class=["w-full"] )
            v-btn(variant="outlined" block rounded="lg" size="x-large" color="primary" @click="close(item)") Cancel
        v-col(class=["w-full"])
            v-btn(variant="elevated" block rounded="lg" size="x-large" color="primary" @click="title_record === 'New Record' ? confirmCreateItem(item) : confirmUpdateItem(item)") Confirm
    
    v-row(v-if="title_record === 'View Details'" class = ["text-size-margin"]) 
        v-col(class=["w-full"] )
            v-btn(variant="elevated" block rounded="lg" size="x-large" color="primary" @click="close(item)") Close
    
            
</template>

<script>
import { defineComponent, ref, computed, onMounted, watch, getCurrentInstance } from 'vue';
import { useRouter } from 'vue-router'
import axios from "axios"
import { useCounterStore } from '../store'

export default defineComponent({
    name: 'EditRecord',
    props: [
        'title_record',
        'closeDialog',
        'save',
        'item'
    ],
    setup(props) {
        const { getItemValue } = useCounterStore()
        const borrower_name = ref('')
        const edited_index = ref("-1")
        const default_book = ref({
            "code": '',
            "name": '',
            "deposit": 0,
        })
        const book_list_local = ref([])
        const newRecord = ref({
            id: '',
            borrower_id: '',
            borrower: '',
            borrow_date: '',
            return_date: '',
            book_list:[],
            total_deposit: '',
            status: ''
        })

        const record = ref({
            "id":'',
            "borrower_id": '',
            "borrow_date": '',
            "return_date": '', 
            "total_deposit": 0, 
            "book_list": [], 
            "status": '',
            "note": '',
        })
        const router = useRouter()
        const rules = (category) => [
            async (value) => {
                if (!value) {
                    return 'Please fill out this required field.'
                }
                if(category){
                    const res = await axios.get(`http://localhost:8000/${category}/${value}`)
                    if(category == "book"){
                        if(res.data.record_id !== 0) { 
                            return "This book is not available"
                        }
                    } 
                    if(!res.data.name) {
                        return  'Please fill out this required field.'
                    }
                    return res.data
                } else return true
            }
        ]

        const select = ref({
            status: '', 
        });
        
        onMounted(async ()  => {
            console.log("item", props.item)
            record.value = props.item
            book_list_local.value = record.value.book_list
            console.log("book_list_local", book_list_local.value)
            
        })
        const total_deposit = computed(() => {
            return book_list_local.value.reduce((sum, item) => sum + parseInt(item.deposit), 0)
        });
        const calculateFee = computed(() => {
            if (record.value.status != "OVERDUE") return 0;
            else return record.value.total_deposit*3;
        })

        watch(()=> record.value.borrower_id, async ()=>{
            console.log(record.value.borrower_id)
            if(record.value.borrower_id){
                await axios.get(`http://localhost:8000/borrower/${record.value.borrower_id}`)
                .then(async (res) =>{
                    console.log("name", res.data.name)
                    borrower_name.value =  res.data.name;
                })
                .catch((error) => {
                    console.log("error")
                    console.error(error)
                })
            } else {
                borrower_name.value =  '';
            }
        })

        const updateNameDeposit = async (item) => {   
            const res = await axios.get(`http://localhost:8000/book/${item.id}`)
            item.name = res.data.name
            item.deposit = res.data.deposit
        }
        

        const goHomePage = () => {
            router.push('/')
        }

        const addItem = () => {
            book_list_local.value.push({
            "id": '',
            "name": '',
            "deposit": '0',
            })
        }

        const deleteItem = (index) => {
            edited_index.value = index
            book_list_local.value.splice(edited_index.value, 1) 
        }
        const close = () => {
            props.closeDialog();
        }
        const confirmCreateItem = async () => {
            axios.post(`http://localhost:8000/record`,{
                borrower_id: record.value.borrower_id,
                borrow_date: record.value.borrow_date,
                return_date: record.value.return_date,
                total_deposit: total_deposit.value,
                status: record.value.status,
                fee:  calculateFee.value,
                note: record.value.note,
                book_list: record.value.book_list
                }).then(async (response) => {
                    await getItemValue();
                    console.log("response", response);
                })
                .catch((error) => {
                    alert(error.message);
                });
            props.save();
        }

        const confirmUpdateItem = async () => {
            axios.patch(`http://localhost:8000/record/${record.value.id}`,{
                    borrower_id: record.value.borrower_id,
                    borrow_date: record.value.borrow_date,
                    return_date: record.value.return_date,
                    total_deposit: total_deposit.value,
                    status: record.value.status,
                    fee:  calculateFee.value, 
                    note: record.value.note,
                    book_list: record.value.book_list
                }).then((response) => {
                    console.log("record.value.book_list", record.value.book_list)
                    console.log(response);
                })
                .catch((error) => {
                    console.error(error)});
            props.save();
        }
        
        return {
            edited_index,
            default_book,
            select,
            goHomePage,
            addItem,
            deleteItem,
            close,
            record,
            confirmCreateItem,
            confirmUpdateItem,
            newRecord,
            total_deposit,
            calculateFee,
            borrower_name,
            updateNameDeposit,
            rules
        };
    },
})
</script>

<style scoped lang="sass">
.text-center 
    display: flex
    align-items: center
    justify-content: center

.no-uppercase 
    text-transform: unset !important
.pa-custom-text
    padding-top: 5px
    padding-bottom: 0px
.pa-custom-field
    padding-top: 0px
    padding-bottom: 0px
.pa-custom-field-book
    margin-top: 5px
    padding-top: 0px
    padding-bottom: 0px

.pa-custom
    padding: 10px 10px 10px 10px

.pa-bot-top
    padding-top: 10px
    padding-bottom: 10px
.card-custom
    variant: "elevated"
    padding: 15px 15px 15px 15px
.v-card-title
    font-size: 25px

.v-data-table-header__content
    font-size: 25px

.custom-disabled 
    color: #000000 !important
    opacity: 100%

.text-size-margin
    font-size: 18px
    margin: 0
</style>