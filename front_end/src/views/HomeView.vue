<template>
  <main class="h-screen flex flex-col">
    <!-- Top Row: Chat Window -->
    <div
      class="h-1/2 p-4 border-2 border-gray-200 rounded-lg dark:border-gray-700 flex flex-col"
    >
      <div class="flex-1 overflow-y-auto mb-4" ref="chatContainer">
        <div v-for="(msg, index) in messages" :key="index" class="mb-2">
          <div :class="msg.isSent ? 'text-right' : 'text-left'">
            <span
              :class="
                msg.isSent ? 'bg-blue-500 text-white' : 'bg-green-400 text-black'
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
          class="flex-1 p-2 border rounded-lg bg-gray-200"
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
    <div class="h-1/2 flex">
      <!-- Left Column: Articles -->
      <div
        class="w-1/2 p-4 border-2 border-gray-200 rounded-lg dark:border-gray-700 m-2"
      >
        <div class="flex justify-between mb-4">
          <h2 class="text-xl">Articles</h2>
          <button class="px-2 py-1 bg-gray-200 rounded-lg">Filter</button>
        </div>
        <ul>
          <li v-for="(article, index) in articles" :key="index" class="mb-2">
            <a :href="article.link" class="text-blue-500">{{ article.title }}</a>
          </li>
        </ul>
      </div>
      <!-- Right Column: Pie Chart -->
      <div
        class="w-1/2 p-4 border-2 border-gray-200 rounded-lg dark:border-gray-700 m-2 flex justify-center items-center"
      >
      <iframe src="https://ourworldindata.org/grapher/cumulative-installed-wind-energy-capacity-gigawatts?tab=chart" loading="lazy" style="width: 100%; height: 600px; border: 0px none;" allow="web-share; clipboard-write"></iframe>
      </div>
    </div>
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
        { title: "Marine Data Exchange Announced New Partnership with Crown Estate Scotland", link: "https://www.marinedataexchange.co.uk/content/stories/crown-estate-scotland-partnership-what-it-all-means" },
        { title: "Baltic Sea countries pledge closer collaboration", link: "https://windeurope.org/newsroom/press-releases/baltic-sea-countries-pledge-closer-collaboration-to-secure-critical-offshore-energy-infrastructure/" },
        { title: "Shell Exits US Offshore Wind Project, Sells Stake to Ocean Winds", link: "https://www.offshorewind.biz/2024/03/21/shell-exits-us-offshore-wind-project-sells-stake-to-ocean-winds/" },
        { title: "Plymouth Marine Laboratory: Offshore wind farms: new paper reveals global impacts on biodiversity and ecosystem services", link: "https://www.pml.ac.uk/news/Offshore-wind-farms-new-paper-reveals-global-impac" },
      ],
      waiting: true,
    };
  },
  components: {
    PieChart: Pie,
  },
  mounted() {
    // this.createPieChart(
    //   "rightPieChart",
    //   ["Solar", "Wind", "Hydro", "Geothermal"],
    //   [25, 35, 25, 15]
    // );
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() === "") return;
      this.waiting = true;
      // Append user message to chat history
      const conversationHistory = this.messages.map(msg => ({
        role: msg.isSent ? 'user' : 'assistant',
        content: msg.text
      }));

      conversationHistory.push({ role: 'user', content: this.newMessage });
      this.newMessage = "";
      // Send the message to the server
      try {
        const response = await fetch(`${this.domain_origin}/send_message`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ conversation_history: conversationHistory }),
        });

        const result = await response.json();

        // Display the complete chat history from the server
        if (response.ok) {
          this.messages = result.conversation_history.map(msg => ({
            text: msg.content,
            isSent: msg.role === 'user'
          }));
          this.waiting = false;
        } else {
          this.messages.push({
            text: "Error: Failed to send message.",
            isSent: false,
          });
          this.waiting = false;
        }
      } catch (error) {
        console.error("Error sending message:", error);
        this.messages.push({
          text: "Error: An error occurred while sending the message.",
          isSent: false,
        });
        this.waiting = false;
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
