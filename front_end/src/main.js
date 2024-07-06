import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css' // Ensure this path is correct

const app = createApp(App)

app.use(router)
app.mount('#app')
// import "bootstrap/dist/css/bootstrap.min.css"
// import "bootstrap/dist/js/bootstrap.js"
// import "bootstrap-icons/font/bootstrap-icons.css";