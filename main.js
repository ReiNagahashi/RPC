const ClientModule = require('./client.js')

const client = new ClientModule.Client('udp4');

client.sendMessage();