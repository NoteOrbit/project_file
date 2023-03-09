
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import sidebar from './components/sidebar.vue'
import sidebar_v2 from './components/sidebar_v2.vue';

import { loadFull } from "tsparticles";

const particlesInit = async engine => {
    await loadFull(engine);
};

const particlesLoaded = async container => {
    console.log("Particles container loaded", container);
};
</script>
<template>
<div class="app">
    <Particles
            id="tsparticles"
            :particlesInit="particlesInit"
            :particlesLoaded="particlesLoaded"

        />

        <Particles
            id="tsparticles"
            :particlesInit="particlesInit"
            :particlesLoaded="particlesLoaded"
            :options="{
                    background: {
                        color: {
                            value: '#FFFFFF'
                        }
                    },
                    fpsLimit: 120,
                    particles: {
                        color: {
                            value: '#000000'
                        },
                        links: {
                            color: '#000000',
                            distance: 150,
                            enable: true,
                            opacity: 0.2,
                            width: 1
                        },
                        collisions: {
                            enable: true
                        },
                        move: {
                            direction: 'none',
                            enable: true,
                            outMode: 'bounce',
                            random: false,
                            speed: 1.5,
                            straight: false
                        },
                        number: {
                            density: {
                                enable: true,
                                area: 800
                            },
                            value: 80
                        },
                        opacity: {
                            value: 0.2
                        },
                        shape: {
                            type: 'circle'
                        },
                        size: {
                            random: true,
                            value: 5
                        }
                    },
                    detectRetina: true
                }"
        />
    <q-layout>
        <sidebar_v2 v-if="!$route.meta.hideNavbar"/>
        <q-page-container>
            <q-page>
                <RouterView/>        
            </q-page>
        </q-page-container>
        
    </q-layout>
    
</div>

</template>


<style>
  /* Add any styles you need here */
</style>