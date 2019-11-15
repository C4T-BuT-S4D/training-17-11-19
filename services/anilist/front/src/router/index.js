import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home";
import Login from "@/views/Login";
import Register from "@/views/Register";
import Player from "@/views/Player";
import Upload from "@/views/Upload";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/login",
    name: "login",
    component: Login
  },
  {
    path: "/register",
    name: "register",
    component: Register
  },
  {
    path: "/anime/upload",
    name: "upload",
    component: Upload
  },
  {
    path: "/anime/:token",
    name: "player",
    component: Player
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
