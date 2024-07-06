<template>
<div class="flex flex-col items-center bg-white shadow-md rounded-lg overflow-hidden p-6">
  <h1 class="text-4xl font-bold mb-4">Add Users</h1>
  <form class="w-1/2">
    <!-- Name input -->
    <div class="relative mb-4">
      <input type="text" id="name" 
             class="form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50" 
             :class="this.users.name_valid" 
             v-model="this.users.new_user.name" 
             @change="this.users.check_name_valid(this.users.new_user.name)" />
      <label for="name" class="absolute top-0 left-0 px-1 -mt-px text-gray-700 bg-white">Name</label>
    </div>

    <!-- Email input -->
    <div class="relative mb-4">
      <input type="text" id="email" 
             class="form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50" 
             :class="this.users.email_valid" 
             v-model="this.users.new_user.email" 
             @change="this.users.check_email_valid(this.users.new_user.email)" />
      <label for="email" class="absolute top-0 left-0 px-1 -mt-px text-gray-700 bg-white">Email address</label>
    </div>

    <!-- Role input -->
    <div class="mb-4">
      <select class="form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50" 
              :class="this.role_valid" 
              @change="this.users.check_role_valid()" 
              aria-label="Role" 
              v-model="this.users.new_user.role">
        <option value="" disabled>Select the role</option>
        <option value="user">User</option>
        <option value="support">Support</option>
        <option value="ho user">ho user</option>
      </select>
    </div>

    <!-- Submit button -->
    <button type="button" class="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 mb-4" 
            @click="this.add_user(); this.users.populate_user_list();">
      Create user
    </button>
  </form>
</div>

<div class="mt-8">
  <div class="flex flex-wrap">
    <div class="w-full">
      <table class="min-w-full divide-y divide-gray-200 table-auto">
        <thead class="bg-gray-800 text-white">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Id #</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Name</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Email</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="user in users.user_list" :key="user.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ user.id }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ user.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ user.email }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <button type="button" class="text-sm bg-green-500 hover:bg-green-700 text-white py-1 px-2 rounded">
                <i class="bi bi-pencil-square"></i> | Edit
              </button>
              <button type="button" class="text-sm bg-red-500 hover:bg-red-700 text-white py-1 px-2 rounded" v-on:click="this.users.delete_user(user.id)">
                <i class="bi bi-trash"></i> | Delete
              </button>
                <button
                  type="button"
                  class="btn btn-primary"
                >
                  <i class="bi bi-unlock"></i>
                  | Unlock</button>
                <button
                  type="button"
                  class="btn btn-warning"
                >
                  <i class="bi bi-shield-lock"></i>
                  | Reset MFA</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      needsVueRefresh: { "data": false, "keepLooping": false },
    };
  },
  methods: {
    add_user() {
      this.users.api_create_user_db();
    },
    vueRefresh() {
      if (
        !(
          ["super user", "ho user", "support"].includes(this.user.role_name) &&
          this.user.logged_in
        )
      ) {
        this.$router.push("login");
      }
      if (this.needsVueRefresh.keepLooping) {
        const myTimeout = setTimeout(this.vueRefresh, 500);
      }
    },
  },
  props: ["users", "user", "roles"],
  created() {
    this.needsVueRefresh.keepLooping = true;
    this.vueRefresh();
    this.users.populate_user_list();
    this.roles.get_roles_from_api();
  },
  beforeUnmount() {
        this.needsVueRefresh.keepLooping = false
  },
};
</script>

<style>
.container {
  padding: 2rem 0rem;
}

td {
  vertical-align: middle;
}

th {
  vertical-align: middle;
}
</style>