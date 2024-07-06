<template>
  <main>
    <div class="mt-3">
      <ul class="list-group">
        <li class="text-3xl">
          Homepage - Scaffolding Template
        </li>
        <li class="list-group-item">
          Please make sure to read through the README for explicit instructions.
        </li>
      </ul>
    </div>
  </main>
</template>

<script>
export default {
  data() {
      return {
          needsVueRefresh: { "data": false, "keepLooping": false },
      }
  },
  props: [
    "user",
    "users"
  ],
  methods: {
    vue_refresh_home() {
      if (!this.user.logged_in) {
        this.$router.push("login");
      }

      if (this.needsVueRefresh.keepLooping) {
        const myTimeout = setTimeout(this.vue_refresh_home, 500);
      }
    },
  },
  created() {
    this.needsVueRefresh.keepLooping = true;
    this.vue_refresh_home();
  },
  beforeUnmount() {
    this.needsVueRefresh.keepLooping = false;
  },
};
</script>