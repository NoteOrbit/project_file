<template>
    <ul>
      <li v-for="item in items">{{ item }}</li>
    </ul>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Example',
    data () {
      return {
        items:[]
      }
    },
    mounted () {
      axios
        .get('https://8a08-2001-fb1-14b-4a38-2d8b-afc0-f89-2a37.ap.ngrok.io/nearby?latitude=123&longitude=123')
        .then(response => {
            console.log(response)
            this.items = response.data
        })
    }
  }
  </script>



<!-- <template>
    <div class="container">
        <div class="form-center">
            <form class="form" method="GET">
                <h1>Try Locations Haversine</h1>
                <div class="line-separator"></div>
                <div class="container-fluid">
                    <input name="latitude" type="float" placeholder="latitude" required />
                    <input name="longitude" type="float" placeholder="longitude" required />
                    <button class="btn btn-outline-success" aria-hidden="true">Find</button>
                </div>
            </form>
        </div>
        <h3>Store Nearby locations</h3>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Store Name</th>
                        <th>Distance</th>
                        <th>Coordinates</th>
                    </tr>
                </thead>
                <ul>
                    <li v-for="item in items" :key="item.id ">{{ item.name }}</li>
                </ul>

            </table>
        </div>
    </div>



</template>


<script>
import axios from 'axios'

export default {
    name: "About",
    data() {
        return {
            items:[]
        }
    },
    mounted() {
        axios
            .get('https://8a08-2001-fb1-14b-4a38-2d8b-afc0-f89-2a37.ap.ngrok.io/nearby?latitude=123&longitude=123')
            .then(response => (this.data = response.data))
    },
}


</script>
<style>

</style> -->
