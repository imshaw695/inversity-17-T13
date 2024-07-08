<script setup>
</script>

<template>
  <div class="min-w-full min-h-full flex flex-col justify-between">
    <Navbar :messages="messages" />
    <Sidebar />
    <div class="p-4 sm:ml-64">
      <RouterView :messages="messages" />
      <footer
      class="bg-white rounded-lg shadow m-4 dark:bg-gray-800 bottom-0 w-full"
      style="z-index: 9999"
    >
      <MessageDisplay v-bind:messages="messages" />
      <div
        class="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between"
      >
        <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400"
          >© 2024
          <a href="https://flowbite.com/" class="hover:underline"
            >Crown Estate</a
          >. All Rights Reserved.
        </span>
        <ul
          class="flex flex-wrap items-center mt-3 text-sm font-medium text-gray-500 dark:text-gray-400 sm:mt-0"
        >
          <li>
            <a href="#" class="hover:underline me-4 md:me-6">About</a>
          </li>
          <li>
            <a href="#" class="hover:underline me-4 md:me-6">Privacy Policy</a>
          </li>
          <li>
            <a href="#" class="hover:underline me-4 md:me-6">Licensing</a>
          </li>
          <li>
            <a href="#" class="hover:underline">Contact</a>
          </li>
        </ul>
      </div>
    </footer>
    </div>
  </div>
</template>

<script>
import { reactive } from "vue";
import { Messages } from "./js/Messages";
import MessageDisplay from "./components/MessageDisplay.vue";
import Navbar from "./components/Navbar.vue";
import Sidebar from "./components/Sidebar.vue";
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
    Sidebar
  },
  methods: {},
};
</script>

<style scoped>
</style>
