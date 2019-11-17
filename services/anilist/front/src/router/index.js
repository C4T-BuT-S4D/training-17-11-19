import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home";
import Login from "@/views/Login";
import Register from "@/views/Register";
import Player from "@/views/Player";
import Upload from "@/views/Upload";
import Uploads from "@/views/MyUploads";
import AnimeList from "@/views/AnimeList";
import MyAnimeList from "@/views/MyAnimeList";
import AddAnime from "@/views/AddAnime";
import AnimeDetail from "@/views/AnimeDetail";

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
    path: "/anime/my",
    name: "uploads",
    component: Uploads
  },
  {
    path: "/anime/list",
    name: "list",
    component: AnimeList
  },
  {
    path: "/anime/mylist",
    name: "myList",
    component: MyAnimeList
  },
  {
    path: "/anime/add",
    name: "animeAdd",
    component: AddAnime
  },
  {
    path: "/anime/:token",
    name: "player",
    component: Player
  },
  {
    path: "/animedetails/:animeId",
    name: "detail",
    component: AnimeDetail
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
