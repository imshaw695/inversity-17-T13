<template>
  <main class="h-screen flex flex-col">
    <!-- Top Row: Chat Window -->
    <!-- Bottom Row -->
    <div class="h-full flex">
      <!-- Left Column: Articles -->
      <div
        class="w-1/2 p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 m-2 flex justify-center items-center"
      >
      <iframe src="https://ourworldindata.org/grapher/wind-generation?tab=map" loading="lazy" style="width: 100%; height: 600px; border: 0px none;" allow="web-share; clipboard-write"></iframe>
      </div>
      <!-- Right Column: Pie Chart -->
      <div
        class="w-1/2 p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 m-2 flex justify-center items-center"
      >
      <iframe src="https://ourworldindata.org/grapher/wind-energy-consumption-vs-installed-wind-energy-capacity?tab=chart" loading="lazy" style="width: 100%; height: 600px; border: 0px none;" allow="web-share; clipboard-write"></iframe>
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
        { title: "Marine Data Exchange Announced New Partnership with Crown Estate Scotland", link: "https://www.marinedataexchange.co.uk/content/stories/crown-estate-scotland-partnership-what-it-all-means" },
        { title: "Baltic Sea countries pledge closer collaboration", link: "https://windeurope.org/newsroom/press-releases/baltic-sea-countries-pledge-closer-collaboration-to-secure-critical-offshore-energy-infrastructure/" },
        { title: "Shell Exits US Offshore Wind Project, Sells Stake to Ocean Winds", link: "https://www.offshorewind.biz/2024/03/21/shell-exits-us-offshore-wind-project-sells-stake-to-ocean-winds/" },
        { title: "Plymouth Marine Laboratory: Offshore wind farms: new paper reveals global impacts on biodiversity and ecosystem services", link: "https://www.pml.ac.uk/news/Offshore-wind-farms-new-paper-reveals-global-impac" },
      ],
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

      // Append user message to chat history
      const conversationHistory = this.messages.map(msg => ({
        role: msg.isSent ? 'user' : 'assistant',
        content: msg.text
      }));

      conversationHistory.push({ role: 'user', content: this.newMessage });

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
