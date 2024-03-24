const ClientModule = require('./client.js')

const client = new ClientModule.Client('udp4');

// サーバにリクエストとしてのメッセージを送信
// client.sendMessage();

// サーバに関数を使用するためのリクエストを送信→json形式で帰ってくることに注意
console.log(client.rpc("floor", 3.5)); // 3
console.log(client.rpc("nroot", 5, 3)); // 3 / 5 = 0.6 
console.log(client.rpc("reverse", "newspaper")); // repapswen
console.log(client.rpc("validAnagram", "adbc@", "bdc@a")); // True
console.log(client.rpc("sort", "dcgeafb".split(""))); // ["a", "b", "c", "d", "e", "f", "g"]





