
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import sidebar from './components/sidebar.vue'
import sidebar_v2 from './components/sidebar_v2.vue';
</script>
<template>
<div class="app">
    <q-layout>
        <sidebar_v2 v-if="!$route.meta.hideNavbar"/>
        <q-page-container>
            <q-page>
                <RouterView/>        
            </q-page>
        </q-page-container>
        
    </q-layout>
    <!-- <q-layout>
        <sidebar_v2/>
        <q-page-container>
            <q-page>
                <sidebar v-if="!$route.meta.hideNavbar"/>
                <RouterView/>    
            </q-page>
            <RouterView/>
        </q-page-container>
    </q-layout> -->
    <!-- <sidebar v-if="!$route.meta.hideNavbar"/>
    <RouterView/> -->



    
</div>

</template>

<script>


</script>
<!-- <style lang="scss">
:root {
    --primary: #cc409b;
    --primary-alt: #223bc5;
    --grey: #64748b;
    --dark: #1e293b;
    --dark-alt: #334155;
    --light: #f1f5f9;
    --sidebar-width: 300px;
}


body {
    background: var(--light);
}

button {
    cursor: pointer;
    appearance: none;
    border: none;
    outline: none;
    background: none;
}

.app {
    display: flex;

    main {
        flex: 1 1 0;
        padding: 2rem;

        @media (max-width: 1300) {
            padding-left: 0rem;
        }
    }
}
</style> -->