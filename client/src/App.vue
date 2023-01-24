
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import sidebar from './components/sidebar.vue'

</script>
<template>
<div class="app">
    <sidebar v-if="!$route.meta.hideNavbar"/>
    <RouterView/>
</div>

</template>

<script>


</script>
<style lang="scss">
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

        @media (max-width: 1024px) {
            padding-left: 6rem;
        }
    }
}
</style>