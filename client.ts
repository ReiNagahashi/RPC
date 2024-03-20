import * as dgram from 'dgram'

// サーバ情報(アドレス、ポート)はグローバル変数としておく(実際にはリクエスト先としてのサーバは複数あるはず。その場合はどう管理するのだろう)
const serverAddress: string = '127.0.0.1';
const serverPort: number = 5000; // サーバーのポート番号

export class Client{
    static clientsCount: number = 1;

    public id: number;
    public socket: dgram.Socket;

    constructor(domainType: dgram.SocketType){
        this.socket = dgram.createSocket(domainType);
        this.id = Client.clientsCount++;
    }

    public sendMessage(): void{
        const prompt = require("prompt-sync")({sigint: true});
        const inputMsg: Buffer = Buffer.from(prompt("Send a message to server"));

        this.bind(inputMsg);
    }

    public bind(msg: Buffer){
        console.log(`Sending message: "${msg}" to ${serverAddress}`);
        this.socket.send(msg, 0, msg.length, serverPort, serverAddress, (err) => {
            if(err){
                console.log("Send Error: ", err);
            }else{
                console.log("Message Sent.");
            }
        })

        // サーバからの応答を待つ
        console.log('Waiting to receive');

        this.socket.on('message', (receivedMessage: Buffer, info: dgram.RemoteInfo) => {
            console.log(`Received message: "${receivedMessage}" from ${info.address}:${info.port}`);

            // ソケットを閉じてリソースを解放
            this.socket.close();
            console.log('Socket closed');
        });
    }

}

// Unixドメインソケットはjsではサポートされていない。
// ここではUDPソケット(IPv4)を使う
// const socket: dgram.Socket = dgram.createSocket('udp4');


// const message: Buffer = Buffer.from('Message to send to the server.');

// socket.bind(() => {
//     // socket.setBroadcast(true);

//     // サーバにメッセージを送信します
//     console.log(`Sending message: "${message}" to ${serverAddress}:${serverPort}`);
//     socket.send(message, 0, message.length, serverPort, serverAddress, (err) => {
//         if (err) {
//             console.error('Send error:', err);
//             socket.close();
//         } else {
//             console.log('Message sent');
//         }
//     });

//     // サーバからの応答を待ち受けます
//     console.log('Waiting to receive');

//     socket.on('message', (receivedMessage: Buffer, info: dgram.RemoteInfo) => {
//         console.log(`Received message: "${receivedMessage}" from ${info.address}:${info.port}`);

//         // ソケットを閉じてリソースを解放します
//         socket.close();
//         console.log('Socket closed');
//     });
// });
