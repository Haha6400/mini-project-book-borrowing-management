
import {createApp} from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";

import router from "./router";

loadFonts();

// router.beforeEach((to, from, next) => {
//   const loggedIn = localStorage.getItem("access_token");
//   if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
//     next("/");
//   } else {
//     next();
//   }
// });
// const confirmed = ref(false);
// Vue.prototype.$confirmed = confirmed


createApp(App).use(router).use(vuetify).mount("#app");
