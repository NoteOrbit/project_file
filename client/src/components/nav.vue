<script setup>

</script>

<template>
  <header>
    <div class="contrainer">
      <nav class="navbar navbar-expand-lg bg-danger">
        <div class="container-fluid">
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01"
            aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
            <a class="navbar-brand" href="/home">Recommendation system</a>
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link class="nav-link no-underline " to="about">
                  Locations base
                </router-link>
              </li>
              <li class="nav-item">

                <a class="nav-link" href="#">Apriori model</a>
              </li>
              <li class="nav-item">
                <a class="nav-link " href="#" tabindex="-1" aria-disabled="true">Fillter</a>
              </li>
              <li class="nav-item">
                <router-link class="nav-link no-underline " to="dashboard">
                 Dashboard
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>
<style>
.no-underline {
  text-decoration: none;
}
</style>
