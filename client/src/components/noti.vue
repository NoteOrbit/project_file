<template>
    <div class="toast-container top-0 end-0 p-3">
      <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" v-if="showToast">
        <div class="toast-header">
          <span class="material-icons">update</span>
          <strong class="me-auto">Notifications</strong>
          <small class="text-muted">just now</small>
          <button type="button" class="btn-close" @click="closeToast" aria-label="Close"></button>
        </div>
        <div class="toast-body">{{ msg }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import $ from 'jquery';
  
  export default {
    props: ['msg'],
    data() {
      return {
        showToast: false
      }
    },
    mounted() {
      if (this.showToast) {
        $('.toast').toast('show');
      }
    },
    methods: {
      closeToast() {
        $('.toast').toast('hide');
        this.showToast = false
      }
    }
  }
  </script>
  