import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import Login from "../views/login.vue";
import Transaction from '../views/Transaction.vue'
import Model from '../views/Model.vue'
import Register from '../views/Register.vue'
import About from '@/views/AboutView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/home",
      name: "home",
      component: HomeView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/login",
      name: "login",
      component: Login,
      meta: {
        hideNavbar: true,
      },
    },
    {
      path: "/Register",
      name: "Register",
      component: Register,
      meta: {
        hideNavbar: true,
      },
    },
    {
      path: "/about",
      name: "about",
      component: About,
    },
    {
      path: "/Transaction",
      name: "Transaction",
      component: Transaction,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/Model",
      name: "Model",
      component: Model,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/:catchAll(.*)*',
      name: "PageNotFound",
      component: () => import("@/views/NotFound.vue"),
      meta: {
        hideNavbar: true,
      },
    },
  ],
});
router.beforeEach((to, from, next) => {
  console.log(localStorage.getItem("token"));
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!localStorage.getItem("token")) {
      next({
        path: "/login",
        query: { redirect: to.fullPath },
      });
    } else {
      next();
    }
  } else {
    next(); // make sure to always call next()!
  }
});

export default router;
