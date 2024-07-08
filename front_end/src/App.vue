<script setup>
</script>

<template>
  <div class="min-w-full min-h-full flex flex-col justify-between">
    <Navbar :messages="messages" />
    <Sidebar />
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
