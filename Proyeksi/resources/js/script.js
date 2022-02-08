import { createApp } from 'vue/dist/vue.esm-browser';
import VueClickAway from "vue3-click-away";

// createApp({
//   data() {
//     return {
//       isDark: localStorage.getItem('theme') === 'dark' ? true : false
//     }
//   },
//   methods: {
//     switcher(event = null) {
//       localStorage.theme = typeof event == 'string' ? event : event.target.checked ? 'dark' : 'light';
//       if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
//         this.isDark = true;
//         document.documentElement.classList.add('dark')
//       } else {
//         this.isDark = false;
//         document.documentElement.classList.remove('dark')
//       }
//     }
//   },
//   mounted() {
//     return this.switcher(localStorage.getItem('theme'));
//   }
// }).mount('#switchTheme')

const dropdownTrigger = createApp({
  data() {
    return {
      open: false
    }
  },
  methods: {
    onClickAway() {
      if (this.open) {
        this.open = false;
      }
    }
  }
})

dropdownTrigger.use(VueClickAway) 
dropdownTrigger.mount('.dropdown-trigger')