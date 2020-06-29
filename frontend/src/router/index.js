import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from "@/components/Main";

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Main
  },
  {
    path: '/:folder_id',
    name: 'Folder',
    component: Main
  }
]

const router = new VueRouter({
  routes
})

export default router
