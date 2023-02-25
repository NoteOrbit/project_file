<script setup>
import box from '../components/box.vue'
import table2 from '../components/table2.vue'
import chart from '../components/bar.vue'
import piechart from '../components/piechart.vue'
import box_count from '../components/box_count.vue'
</script>

<template>
    <!-- <navbar /> -->

    
            
                <div class="q-pa-md ">
                    <div class="rounded">
                        <h2 class="flex flex-center text-white">Welcome {{ currentUser }} 👨🏻‍💻</h2>
                    </div>
                    <div>
                        <box />
                    </div>



                    <!-- 
                            <q-row>
                                <q-col >
                                    <q-responsive :ratio="1">
                                <piechart  />
                            </q-responsive>
                                </q-col>
                                <q-col>
                                    <q-responsive :ratio="1">
                                        <chart/>
                            </q-responsive>
                                </q-col>


                                
                            </q-row> -->
                    <div class="q-pa-md">
                        <div class="row items-start q-gutter-md">
                            <q-responsive :ratio="1" class="col" style="width: 500px; max-width: 100%;">
                                <q-card class="column flex flex-center q-pa-md" >
                                     
                                    <piechart/>
        
                                </q-card>
                            </q-responsive>
                            
                            <q-responsive :ratio="1" class="col" style="width: 500px; max-width: 100%;">
                                <q-card class="column flex flex-center q-pa-md">
                                    <chart />
                                    
                                </q-card> 
                            </q-responsive>
                        </div>
                    </div>
                    <div>
                        <box_count/>
                    </div>
                </div>

    
</template>
<script>
import axios from '../axios.js';
import '../assets/style.css'
import { mapGetters } from 'vuex'

export default {
    components: {
        piechart
    },
    computed: {
        ...mapGetters(['currentUser'])
    },
    name: "Home",
    data() {
        return {

        }
    },

}
</script>
<style>
.rounded {
    background-color: rgb(156, 169, 181);
    padding: 20px;
    margin-bottom: 10px;
    border-radius: 10px 10px 10px 10px;
}
</style>
