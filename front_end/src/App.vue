<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-lg text-center">
      <h1 class="text-3xl font-bold mb-4 text-gray-800">Inversity Team 13</h1>
      <p class="text-gray-600 mb-6">
        Crown Estate Hackathon
      </p>
      <div class="mb-4">
        <input v-model="message" type="text" class="w-full p-2 border rounded mb-2" placeholder="Write a message">
        <button @click="sendMessage" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Send
        </button>
      </div>
      <div>
      {{ this.domain_origin }}
      </div>
      <div v-if="responseMessage" class="mt-4 p-4 bg-gray-200 rounded">
        <p class="text-gray-800">{{ responseMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
      responseMessage: '',
      domain_origin: ''
    };
  },
  created() {
    this.domain_origin = window.location.origin;
    if (this.domain_origin.slice(-5) == ":5173") {
      this.domain_origin = this.domain_origin.replace(":5173", ":5000");
    }
  },
  methods: {
    async sendMessage() {
      try {
        const response = await fetch(`${this.domain_origin}/test`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: this.message })
        });
        const result = await response.json();
        if (response.ok) {
          this.responseMessage = result.message;
        } else {
          this.responseMessage = 'Failed to send message.';
        }
      } catch (error) {
        console.error('Error sending message:', error);
        this.responseMessage = 'An error occurred while sending the message.';
      }
    }
  }
};
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
