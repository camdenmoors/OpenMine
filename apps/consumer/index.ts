import {Event} from "./types/Event";
import config from '../../config.json'
import amqp, {Message} from 'amqplib/callback_api'
import _ from 'lodash'

function processEvent(message: Message) {
    if (message.content) {
        try {
            const data: Event = JSON.parse(message.content.toString());
            console.log(_.omit(data))
        } catch {
            console.log("Invalid Message: %s", message.content)
        }

    } else {
        console.log("Missing message")
    }

}

amqp.connect(`amqp://${config.amqp.host}`, (error0, connection) => {
    if (error0) {
        throw error0;
    }
    connection.createChannel((error1, channel) => {
        if (error1) {
            throw error1;
        }

        channel.assertQueue(config.amqp.queue, {
            durable: false
        });


        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", config.amqp.queue);

        channel.consume(config.amqp.queue, processEvent, {
            noAck: true
        });
    });
});