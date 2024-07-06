export class Messages {
    constructor() {
        console.log("Messages has been instantiated.")
        this.message_array = []
        // this.current_message = {};
    }

    add_message(message, type) {
        let message_dict = {};
        message_dict.message = message;
        message_dict.type = type;
        this.message_array.push(message_dict);
        return this.message_array;
    }
}