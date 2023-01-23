<template>

    <div class="container h-100 my-5">
        <div class="row d-flex justify-content-center align-items-center h-100">
            <div class="col-lg-12 col-xl-11">
                <div class="card text-black" style="border-radius: 25px;">
                    <div class="card-body p-md-5">
                        <div class="row justify-content-center">
                            <div class="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">

                                <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Register</p>
                                <form @submit.prevent="register">
                                    <div class="form-group">
                                        <label for="username">Username</label>
                                        <input type="text" id="username" v-model="username" class="form-control" />
                                    </div>
                                    <div class="form-group">
                                        <label for="name">Name</label>
                                        <input type="text" id="name" v-model="name" class="form-control" />
                                    </div>
                                    <div class="form-group">
                                        <label for="email">Email</label>
                                        <input type="email" id="email" v-model="email" class="form-control" />
                                    </div>
                                    <div class="form-group">
                                        <label for="password">Password</label>
                                        <input type="password" id="password" v-model="password" class="form-control" />
                                    </div>
                                
                                    <button class="btn btn-primary" type="submit">Register</button>
                                </form>



                            </div>
                            <div class="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2">

                                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/draw1.webp"
                                    class="img-fluid" alt="Sample image">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
        <h1>Register</h1>

        <form @submit.prevent="register">
            <div class="form-group">
                <label for="password">Username</label>
                <input type="password" id="password" v-model="Username" class="form-control" />
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" v-model="email" class="form-control" />
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" class="form-control" />
            </div>

            <button class="btn btn-primary" type="submit">Register</button>
        </form>
    </div> -->
</template>

<script>
import axios from '../axios.js'

export default {
    data() {
        return {
            username: '',
            name:'',
            email: '',
            password: '',
            response: ''
        }
    },
    methods: {
        register() {
            axios.post('/Register', {
                username: this.username,
                name:this.name,
                email: this.email,
                password: this.password
            })
                .then(response => {
                    this.response = response.status
                    if(response.status === 201){
                        this.$router.push({name:'login'})
                    }
                    // Do something with the response, like redirecting to the login page
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>