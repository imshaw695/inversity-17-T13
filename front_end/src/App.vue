<script setup>
</script>

<template>
  <div class="min-w-full min-h-full flex flex-col justify-between">
    <Navbar :user="user" :messages="messages" :roles="roles" v-if="(this.user.logged_in)" />
    <RouterView
    :users="users"
    :user="user"
    :roles="roles"
    :messages="messages"
    />
    <!-- These breaks stop the bottom of the page content from disapearing behind the fixed footer -->
    <div><br> <br> <br> </div>
    <footer class="fixed bottom-0 w-full bg-gray-900 text-white py-1" style="z-index: 9999;">
      <MessageDisplay v-bind:messages="messages"/>
      <hr class="mx-4 my-1">
      <div class="flex justify-between">
        <p class="mx-3 my-1">
            For support, please email us at: support@thebigteam.co.uk
            <!-- IP Address: {{ this.user.ip_address }} -->
          </p>
          <p class="mx-3 my-1">
            <i className="icon bi-c-circle ms-0 ps-0" style="font-size: 1.0rem;"></i> 2023 - dt-squad Ltd&nbsp
          </p>
      </div>
      <hr class="mx-4 my-1">
    </footer>
  </div>
</template>

<script>
import { reactive } from "vue";
import { User } from "./js/User";
import { Users } from "./js/Users";
import { Messages } from "./js/Messages";
import MessageDisplay from "./components/MessageDisplay.vue";
import Navbar from "./components/Navbar.vue"
import Roles from "./js/Roles";
// import { useRoute } from 'vue-router';
export default {
  data() {
    return {
      users: {},
      user: {},
      messages: {},
      roles: {},
      // needsVueRefresh: { "data": false, "keepLooping": false },
    }
  },
  created() {
    let domain_origin = window.location.origin
    if (domain_origin.slice(-5) == ":5173") {
      domain_origin = domain_origin.replace(":5173", ":5000")
    }
    const messages = reactive(new Messages());
    const user = reactive(new User(messages, domain_origin));
    const roles = reactive(new Roles(domain_origin, user));
    const users = reactive(new Users(user, messages, domain_origin, roles));
    this.user = user;
    this.roles = roles;
    this.users = users;
    this.messages = messages;
    this.check_invalid_token();
    this.check_token_validity();
    // this.needsVueRefresh.keepLooping = true;
    // this.check_logged_in();
    // this.vueRefresh()
  },
  components: {
    MessageDisplay,
    Navbar
  },
  methods: {
    check_invalid_token() {
        if (this.user.invalid_token == true) {
                this.user.logout()
                this.messages.add_message("Session expired, please login.", "text-danger h6");
                this.$router.push({ name: "login" });
                this.user.logged_in = true;
                this.user.invalid_token = false;
        }
        setTimeout(this.check_invalid_token, 2000)
      },
    check_token_validity() {
      if (this.user.logged_in == true) {
        this.user.check_token_validity();
      }
      setTimeout(this.check_token_validity, 30000)
    },
    vue_refresh() {
            try {
                this.needs_vue_refresh.data = this.user.ip_address
            } catch (error) {

            }

            if (this.needs_vue_refresh.keep_looping) {
                const my_timeout = setTimeout(this.vue_refresh, 500);
            }
        },    
    check_logged_in() {
      // this.users.current_user = this.user.check_logged_in();
      if (!(this.user.logged_in) && !(this.$router.name=="passwordreset") ) {
        this.$router.push("login")
      }
      setTimeout(this.check_logged_in, 5000);
    },
  }
}
</script>

<style scoped>
</style>
