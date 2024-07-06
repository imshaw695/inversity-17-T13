<template>
<div class="absolute bottom-0 left-0 w-full">
<ul class="mb-3">
    <li class="flex justify-between items-center py-1 px-2 bg-white border-b border-gray-200" 
        :class="{
          'bg-blue-100': message.type === 'info', 
          'bg-green-100': message.type === 'success',
          'bg-yellow-100': message.type === 'warning',
          'bg-red-100': message.type === 'error'
        }" 
        v-for="(message, index) in this.messages.message_array" :key="index">
        <span>
            {{ message.message }}
        </span>
        <button type="button" class="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 font-medium rounded-lg text-sm p-1.5 text-center inline-flex items-center mr-2" @click="this.delete_message(index)">X</button>
    </li>
</ul>
</div>
</template>

<script>
export default {
    props: [
        "messages"
    ],
    methods: {
        delete_message(index) {
            this.messages.message_array.splice(index,1);
        }
        // message_cycle() {
        //     console.log("message_cycle")
        //     this.messages.current_message = {};
        //     if (this.messages.message_array.length > 0) {
        //         for (let message_index in this.messages.message_array) {
        //             this.messages.current_message = this.messages.message_array[message_index];
        //         }
        //     }
        //     setTimeout(this.message_cycle, 2000);
        // }
    },
}
</script>