#!/usr/bin/env node

import amqp from 'amqplib/callback_api'
import _ from 'lodash'

function handleMessage(message: amqp.Message) {
    if (message.content) {
        try {
            const messageJson = JSON.parse(message.content.toString())
            console.log(_.omit(messageJson, ['_raw']))
        } catch {
            console.log("Invalid message %s", message.content)
        }
    } else {
        console.log("No content")
    }
}

amqp.connect('amqp://localhost', function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel) {
        if (error1) {
            throw error1;
        }

        var queue = 'main_queue';

        channel.assertQueue(queue, {
            durable: false
        });

        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);

        channel.consume(queue, handleMessage, {
            noAck: true
        });
    });
});