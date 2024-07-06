<script setup>
</script>

<template>
  <div class="min-w-full min-h-full flex flex-col justify-between">
    <Navbar :messages="messages" />

    <button
      data-drawer-target="default-sidebar"
      data-drawer-toggle="default-sidebar"
      aria-controls="default-sidebar"
      type="button"
      class="inline-flex items-center p-2 mt-2 ms-3 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
    >
      <span class="sr-only">Open sidebar</span>
      <svg
        class="w-6 h-6"
        aria-hidden="true"
        fill="currentColor"
        viewBox="0 0 20 20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          clip-rule="evenodd"
          fill-rule="evenodd"
          d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
        ></path>
      </svg>
    </button>

    <aside
      id="default-sidebar"
      class="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0"
      aria-label="Sidebar"
    >
      <div class="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
        <ul class="space-y-2 font-medium">
          <!-- Main Link 1 -->
          <li>
            <a
              href="#"
              class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
            >
              <svg
                class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 21"
              >
                <path
                  d="M16.975 11H10V4.025a1 1 0 0 0-1.066-.998 8.5 8.5 0 1 0 9.039 9.039.999.999 0 0 0-1-1.066h.002Z"
                />
                <path
                  d="M12.5 0c-.157 0-.311.01-.565.027A1 1 0 0 0 11 1.02V10h8.975a1 1 0 0 0 1-.935c.013-.188.028-.374.028-.565A8.51 8.51 0 0 0 12.5 0Z"
                />
              </svg>
              <span class="ms-3">Analytics</span>
            </a>
            <ul class="ml-6 mt-1 space-y-1">
              <li @click="$router.push('dashboard')">
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >- Global Wind Energy Dashboard</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >- Biodiversity Dashboard</a
                >
              </li>
            </ul>
          </li>
          <!-- Main Link 2 -->
          <li>
            <a
              href="#"
              class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
            >
              <svg
                class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 18 18"
              >
                <path
                  d="M6.143 0H1.857A1.857 1.857 0 0 0 0 1.857v4.286C0 7.169.831 8 1.857 8h4.286A1.857 1.857 0 0 0 8 6.143V1.857A1.857 1.857 0 0 0 6.143 0Zm10 0h-4.286A1.857 1.857 0 0 0 10 1.857v4.286C10 7.169 10.831 8 11.857 8h4.286A1.857 1.857 0 0 0 18 6.143V1.857A1.857 1.857 0 0 0 16.143 0Zm-10 10H1.857A1.857 1.857 0 0 0 0 11.857v4.286C0 17.169.831 18 1.857 18h4.286A1.857 1.857 0 0 0 8 16.143v-4.286A1.857 1.857 0 0 0 6.143 10Zm10 0h-4.286A1.857 1.857 0 0 0 10 11.857v4.286c0 1.026.831 1.857 1.857 1.857h4.286A1.857 1.857 0 0 0 18 16.143v-4.286A1.857 1.857 0 0 0 16.143 10Z"
                />
              </svg>
              <span class="flex-1 ms-3 whitespace-nowrap">Articles</span>
            </a>
            <ul class="ml-6 mt-1 space-y-1">
              <li>
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >- The Future of Offshore Wind Farms and Renewable Energy</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >- Advancements in Wind Turbine Design Boosting Efficiency</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >- AI and Big Data Optimizing Wind Farm Operations</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >Local Wind Farms Empowering Towns and Reducing Carbon
                  Footprints</a
                >
              </li>
            </ul>
          </li>
          <!-- Main Link 3 -->
          <li>
            <a
              href="#"
              class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
            >
              <svg
                class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  d="m17.418 3.623-.018-.008a6.713 6.713 0 0 0-2.4-.569V2h1a1 1 0 1 0 0-2h-2a1 1 0 0 0-1 1v2H9.89A6.977 6.977 0 0 1 12 8v5h-2V8A5 5 0 1 0 0 8v6a1 1 0 0 0 1 1h8v4a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-4h6a1 1 0 0 0 1-1V8a5 5 0 0 0-2.582-4.377ZM6 12H4a1 1 0 0 1 0-2h2a1 1 0 0 1 0 2Z"
                />
              </svg>
              <span class="flex-1 ms-3 whitespace-nowrap"
                >Data Integration</span
              >
            </a>
            <!-- <ul class="ml-6 mt-1 space-y-1">
              <li>
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >- Sub Link 3.1</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >- Sub Link 3.2</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="block p-2 text-gray-700 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                  >- Sub Link 3.3</a
                >
              </li>
            </ul> -->
          </li>
          <li>
            <a
              href="#"
              class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
            >
              <svg
                class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  d="M12 8.00002C10.343 8.00002 9 9.34301 9 11C9 12.657 10.343 14 12 14C13.657 14 15 12.657 15 11C15 9.34301 13.657 8.00002 12 8.00002ZM21.82 14.54C21.94 14.06 22 13.54 22 13C22 12.46 21.94 11.94 21.82 11.46L23.75 9.6C24.02 9.32 24.08 8.86 23.91 8.48L21.91 4.52C21.73 4.14 21.31 3.96 20.91 4.04L18.24 4.64C17.69 4.25 17.1 3.92 16.46 3.67L16 1C15.92 0.58 15.53 0.25 15.09 0.25H8.91001C8.47001 0.25 8.08001 0.58 8.00001 1L7.54001 3.67C6.90001 3.92 6.31001 4.25 5.76001 4.64L3.09001 4.04C2.69001 3.96 2.27001 4.14 2.09001 4.52L0.0900116 8.48C-0.0799884 8.86 -0.0199884 9.32 0.240012 9.6L2.18001 11.46C2.06001 11.94 2.00001 12.46 2.00001 13C2.00001 13.54 2.06001 14.06 2.18001 14.54L0.240012 16.4C-0.0199884 16.68 -0.0799884 17.14 0.0900116 17.52L2.09001 21.48C2.27001 21.86 2.69001 22.04 3.09001 21.96L5.76001 21.36C6.31001 21.75 6.90001 22.08 7.54001 22.33L8.00001 25C8.08001 25.42 8.47001 25.75 8.91001 25.75H15.09C15.53 25.75 15.92 25.42 16 25L16.46 22.33C17.1 22.08 17.69 21.75 18.24 21.36L20.91 21.96C21.31 22.04 21.73 21.86 21.91 21.48L23.91 17.52C24.08 17.14 24.02 16.68 23.75 16.4L21.82 14.54ZM12 17C8.69001 17 6.00001 14.31 6.00001 11C6.00001 7.69001 8.69001 5.00001 12 5.00001C15.31 5.00001 18 7.69001 18 11C18 14.31 15.31 17 12 17Z"
                />
              </svg>

              <span class="flex-1 ms-3 whitespace-nowrap">Settings</span>
            </a>
          </li>
        </ul>
      </div>
    </aside>

    <div class="p-4 sm:ml-64">
      <RouterView :messages="messages" />
    </div>
  </div>
</template>

<script>
import { reactive } from "vue";
import { Messages } from "./js/Messages";
import MessageDisplay from "./components/MessageDisplay.vue";
import Navbar from "./components/Navbar.vue";
export default {
  data() {
    return {
      messages: {},
    };
  },
  created() {
    let domain_origin = window.location.origin;
    if (domain_origin.slice(-5) == ":5173") {
      domain_origin = domain_origin.replace(":5173", ":5000");
    }
    const messages = reactive(new Messages());
    this.messages = messages;
  },
  components: {
    MessageDisplay,
    Navbar,
  },
  methods: {},
};
</script>

<style scoped>
</style>
