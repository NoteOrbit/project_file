<template>
    <div class="container text-center  mt-5 mb-5">
        <h1 class="mt-5 fw-bolder text-success "> API FETCH </h1>
        <div class="table-responsive my-5">

            <!-- The table component -->
            <Table :fields='fields' :studentData="items"></Table>
        </div>

    </div>
</template>

<script>
import Table from '../components/table.vue'
import axios from '../axios.js'
export default {
  name: 'Trainsactions',
  data () {
    return {
        items: [],
        fields: ['store','distance','latitude','longitude'],
        setup(){
            axios
            .get('/recomnear?latitude=123&longitude=123')
            .then(response => {
                console.log(response)
                this.items = response.data
            });
        }
    }
  },
  mounted () {
    this.setup()
  },
  components: {
    Table
  }
}
</script>