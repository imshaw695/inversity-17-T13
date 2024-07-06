<template>
  <main class="h-screen flex flex-col">
    <!-- Top Row: Chat Window -->
    <div
      class="h-2/3 p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 flex flex-col"
    >
      <div class="flex-1 overflow-y-auto mb-4" ref="chatContainer">
        <div v-for="(msg, index) in messages" :key="index" class="mb-2">
          <div :class="msg.isSent ? 'text-right' : 'text-left'">
            <span
              :class="
                msg.isSent ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'
              "
              class="inline-block px-4 py-2 rounded-lg"
            >
              {{ msg.text }}
            </span>
          </div>
        </div>
      </div>
      <div class="flex">
        <input
          v-model="newMessage"
          type="text"
          class="flex-1 p-2 border rounded-lg"
          placeholder="Type your message"
          @keyup.enter="sendMessage"
        />
        <button
          @click="sendMessage"
          class="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Send
        </button>
      </div>
    </div>

    <!-- Bottom Row -->
    <div class="h-1/3 flex">
      <!-- Left Column: Articles -->
      <div
        class="w-1/2 p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 m-2"
      >
        <div class="flex justify-between mb-4">
          <h2 class="text-xl">Articles</h2>
          <button class="px-2 py-1 bg-gray-200 rounded-lg">Filter</button>
        </div>
        <ul>
          <li v-for="(article, index) in articles" :key="index" class="mb-2">
            <a href="#" class="text-blue-500">{{ article.title }}</a>
          </li>
        </ul>
      </div>
      <!-- Right Column: Pie Chart -->
      <div
        class="w-1/2 p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 m-2 flex justify-center items-center"
      >
        <canvas id="rightPieChart"></canvas>
      </div>
    </div>
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
  </main>
</template>

<script>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from "chart.js";

ChartJS.register(Title, Tooltip, Legend, ArcElement);

export default {
  data() {
    return {
      newMessage: "",
      messages: [],
      domain_origin: "",
      articles: [
        { title: "Article 1: The Future of Wind Energy" },
        { title: "Article 2: Benefits of Offshore Wind Farms" },
        { title: "Article 3: Innovations in Clean Energy" },
        { title: "Article 4: How Wind Energy Works" },
      ],
    };
  },
  components: {
    PieChart: Pie,
  },
  mounted() {
    this.createPieChart(
      "rightPieChart",
      ["Solar", "Wind", "Hydro", "Geothermal"],
      [25, 35, 25, 15]
    );
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() === "") return;

      // Add the new message to the chat window
      this.messages.push({ text: this.newMessage, isSent: true });

      // Send the message to the server
      try {
        const response = await fetch(`${this.domain_origin}/send_message`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: this.newMessage }),
        });

        const result = await response.json();

        // Display the response message from the server
        if (response.ok) {
          this.messages.push({ text: result.message, isSent: false });
        } else {
          this.messages.push({
            text: "Error: Failed to send message.",
            isSent: false,
          });
        }
      } catch (error) {
        console.error("Error sending message:", error);
        this.messages.push({
          text: "Error: An error occurred while sending the message.",
          isSent: false,
        });
      }

      // Clear the input field
      this.newMessage = "";

      // Scroll to the bottom of the chat container
      this.$nextTick(() => {
        const chatContainer = this.$refs.chatContainer;
        chatContainer.scrollTop = chatContainer.scrollHeight;
      });
    },
    createPieChart(chartId, labels, data) {
      new ChartJS(document.getElementById(chartId).getContext("2d"), {
        type: "pie",
        data: {
          labels: labels,
          datasets: [
            {
              data: data,
              backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Clean Energy Sources",
            },
          },
        },
      });
    },
  },
  created() {
    this.domain_origin = window.location.origin;
    if (this.domain_origin.slice(-5) == ":5173") {
      this.domain_origin = this.domain_origin.replace(":5173", ":5000");
    }
  },
};
</script>

<style scoped>
/* Add any additional styles if necessary */
</style>
