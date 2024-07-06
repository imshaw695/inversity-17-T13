<template>
  <main class="h-screen flex flex-col">
    <!-- Top Row: Chat Window -->
    <div class="h-1/3 p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 flex flex-col">
      <div class="flex-1 overflow-y-auto mb-4" ref="chatContainer">
        <div v-for="(msg, index) in messages" :key="index" class="mb-2">
          <div :class="msg.isSent ? 'text-right' : 'text-left'">
            <span :class="msg.isSent ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'" class="inline-block px-4 py-2 rounded-lg">
              {{ msg.text }}
            </span>
          </div>
        </div>
      </div>
      <div class="flex">
        <input v-model="newMessage" type="text" class="flex-1 p-2 border rounded-lg" placeholder="Type your message" @keyup.enter="sendMessage">
        <button @click="sendMessage" class="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">Send</button>
      </div>
    </div>

    <!-- Bottom Row -->
    <div class="h-2/3 flex">
      <!-- Left Column -->
      <div class="w-1/2 p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 m-2">
        <canvas id="leftPieChart"></canvas>
      </div>
      <!-- Right Column -->
      <div class="w-1/2 p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 m-2">
        <canvas id="rightPieChart"></canvas>
      </div>
    </div>
  </main>
</template>

<script>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

export default {
  data() {
    return {
      newMessage: '',
      messages: [],
      domain_origin: ''
    };
  },
  components: {
    PieChart: Pie
  },
  mounted() {
    this.createPieChart('leftPieChart', ['Solar', 'Wind', 'Hydro', 'Geothermal'], [30, 40, 20, 10]);
    this.createPieChart('rightPieChart', ['Solar', 'Wind', 'Hydro', 'Geothermal'], [25, 35, 25, 15]);
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() === '') return;

      // Add the new message to the chat window
      this.messages.push({ text: this.newMessage, isSent: true });

      // Send the message to the server
      try {
        const response = await fetch(`${this.domain_origin}/send_message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: this.newMessage })
        });

        const result = await response.json();

        // Display the response message from the server
        if (response.ok) {
          this.messages.push({ text: result.message, isSent: false });
        } else {
          this.messages.push({ text: 'Error: Failed to send message.', isSent: false });
        }
      } catch (error) {
        console.error('Error sending message:', error);
        this.messages.push({ text: 'Error: An error occurred while sending the message.', isSent: false });
      }

      // Clear the input field
      this.newMessage = '';

      // Scroll to the bottom of the chat container
      this.$nextTick(() => {
        const chatContainer = this.$refs.chatContainer;
        chatContainer.scrollTop = chatContainer.scrollHeight;
      });
    },
    createPieChart(chartId, labels, data) {
      new ChartJS(document.getElementById(chartId).getContext('2d'), {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Clean Energy Sources'
            }
          }
        }
      });
    }
  },
  created() {
    this.domain_origin = window.location.origin;
    if (this.domain_origin.slice(-5) == ":5173") {
      this.domain_origin = this.domain_origin.replace(":5173", ":5000");
    }
  }
};
</script>

<style scoped>
/* Add any additional styles if necessary */
</style>
