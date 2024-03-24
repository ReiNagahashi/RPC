"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Client = void 0;
var dgram = require("dgram");
// サーバ情報(アドレス、ポート)はグローバル変数としておく(実際にはリクエスト先としてのサーバは複数あるはず。その場合はどう管理するのだろう)
var serverAddress = '127.0.0.1';
var serverPort = 5000; // サーバーのポート番号
var Client = /** @class */ (function () {
    function Client(domainType) {
        this.socket = dgram.createSocket(domainType);
        this.id = Client.clientsCount++;
    }
    Client.prototype.sendMessage = function () {
        var prompt = require("prompt-sync")({ sigint: true });
        var inputMsg = Buffer.from(prompt("Send a message to server"));
        this.bind(inputMsg);
    };
    // rpc(関数名, 引数1, 引数2, ..., 引数n)
    Client.prototype.rpc = function (methodName) {
        var params = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            params[_i - 1] = arguments[_i];
        }
        var methodObj = {
            "method": methodName,
            "params": params,
            "param_types": params.map(function (param) { return typeof param; }),
            "id": this.id
        };
        var jsonData = JSON.stringify(methodObj);
        this.bind(Buffer.from(jsonData));
    };
    Client.prototype.bind = function (msg) {
        var _this = this;
        console.log("Sending request: \"".concat(msg, "\" to ").concat(serverAddress));
        this.socket.send(msg, 0, msg.length, serverPort, serverAddress, function (err) {
            if (err) {
                console.log("Send Error: ", err);
            }
            else {
                console.log("Request Sent");
            }
        });
        // サーバからの応答を待つ
        // console.log('Waiting to receive');
        this.socket.on('message', function (receivedMessage, info) {
            console.log("Received result: \"".concat(receivedMessage, "\" from ").concat(info.address, ":").concat(info.port));
            // ソケットを閉じてリソースを解放
            _this.socket.close();
            console.log('Socket closed');
        });
    };
    // クラス変数とも呼ぶみたい
    Client.clientsCount = 1;
    return Client;
}());
exports.Client = Client;
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
