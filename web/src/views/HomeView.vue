<script setup>
import navbar from '../components/nav.vue'
</script>


<template>
<navbar/>
<div class="jumbotron jumbotron-fluid">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <img src="https://static.fandomspot.com/images/05/6906/06-battle-programmer-shirase-anime.jpg" alt="your_image_description" class="img-radius-right">
            <h1 class="display-4">Recommendation Project</h1>
            <p class="lead">Progress Work By Note Chu<br>Co-Developer Warit Anan <br> Front end developer Narongrit Uppa <br> Assistant Sasiwimol Thong</p>
          </div>
          <div class="col-md-6">
            <p class="display-4">Goal</p>
            <p class="lead">We try to build it from the data collected in Google Form and Another way to create
              The system applies to the applications.</p>
        </div>
        </div>
      </div>
  </div>
<div class="container"> 
<div class="alert alert-success" role="alert">
  <h4 class="alert-heading">Welcome</h4>
  <p>We are very pleased that you visit our website, but at this time our website is in the developing and studying stages recommendations system.</p>
  <hr>
  <p class="mb-0">We will continue to develop and bring progress here.</p>
</div>
<h1>Try to doing</h1>
<ul>
    <li>martix factorizations</li>
    <div class="progress">
        <div class="progress-bar bg-success" role="progressbar" style="width: 50%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
    <li>apriori algorithm</li>
    <div class="progress">
        <div class="progress-bar bg-info" role="progressbar" style="width: 40%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
    <li>Popularity</li>
    <div class="progress">
        <div class="progress-bar bg-warning" role="progressbar" style="width: 70%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
    <li>knn algorithm</li>
    <div class="progress">
        <div class="progress-bar bg-danger" role="progressbar" style="width: 50%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
    <li>Singular value decomposition</li>
    <div class="progress">
        <div class="progress-bar" role="progressbar" style="width: 30%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
    <li>locations base haversine</li>
    <div class="progress">
        <div class="progress-bar bg-success" role="progressbar" style="width: 100%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
    <li>design db mongodb and firebase</li>
    <div class="progress">
        <div class="progress-bar bg-info" role="progressbar" style="width: 40%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
    <li>create api with flask</li>
    <div class="progress">
        <div class="progress-bar bg-warning" role="progressbar" style="width: 39%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
    <li>try to connect</li>
    <div class="progress">
        <div class="progress-bar bg-danger" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
  </ul>
</div>   
<!-- </style> -->

</template>

<style>
.form-center {
    display: flex;
    justify-content: center;
    align-items: center;
}

.img-radius-right {
    border-top-right-radius: 50%;
    border-bottom-right-radius: 50%;
    max-width: 30%;
    height: auto;
      
}

.card-container{
    padding: 5px;
  }


td {
    overflow: hidden;
    text-overflow: ellipsis;
}

@media (max-width: 768px) {
    td {
        overflow: visible;
        white-space: normal;
        word-wrap: break-word;
    }
}
</style>
