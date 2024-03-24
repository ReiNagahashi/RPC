# サーバクラスを作る
# コンストラクターではサーバアドレス・ポートを渡す(ソケットドメインがUNIXの場合は、ポート情報は不要なので別にクラスを作る必要がある？)
# レシーブメソッドではクライアントのアドレスを静的データとしての配列に格納する。この時、リクエスト内のidをインデックスとして指定する。
# センドデータでは配列に入っているリクエストを
# リクエストでくるidを固定配列のインデックスにする

# import os
import socket
import math
import json

class Server:
    # 固定サイズの配列でクライアントのアクセス数制限をする→空でない場合はそのidにクライアントのアドレスがあることを意味している
    clients = [""]*10
    maximumDataSize = 4096

    def __init__(self, socketFamily, socketType, serverIP, serverPort) -> None:
        self.socket = socket.socket(socketFamily, socketType)
        self.address = (serverIP, serverPort)
        print(f"Server is running on {serverIP}:{serverPort}")
        

    def bind(self) -> None:
        self.socket.bind(self.address)

    @staticmethod
    def parseToDict(data) -> dict:
        # バイトデータを文字列に変換
        jsonString = data.decode('utf-8')
        # 文字列データをディクショナリに変換
        try:
            dataDict = json.loads(jsonString)
            return dataDict

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        

    def receiveRequest(self) -> None:
        while True:
            print('\nwaiting to recieve massege')
            data, address = self.socket.recvfrom(self.maximumDataSize)
            # JSONデータを受け取るので、JSオブジェクトにパースする必要がある
            dictData = Server.parseToDict(data)
            assert dictData != None, "Error Occured at converting dict data"
            print('received {} bytes from {}'.format(len(dictData), address[0]))
            if dictData["id"] > len(self.clients) or len(dictData) > self.maximumDataSize:
                print("Error Occured!")
                return

            self.clients[dictData["id"]] = address

            if dictData:
                # responseはJSON形式として渡される
                response = self.createResponse(dictData)
                # sendtoメソッドの引数として渡すデータはJSONのままではダメ。代わりにbyte形式にしてあげる必要がある
                sent = self.socket.sendto(response.encode(), address)
                print('sent {} bytes back to {}'.format(sent, address))

    @staticmethod
    def validateParamsType(paramTypes, expectedParamTypes) -> bool:
        return paramTypes == expectedParamTypes

    @staticmethod
    def createResponse(data) -> str:
        # floor(double x): 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
        # nroot(int n, int x): 方程式 rn = x における、r の値を計算する。
        # reverse(string s): 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
        # validAnagram(string str1, string str2): 2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
        # sort(string[] strArr): 文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。
        
        # ディクショナリを用意して関数を管理する。関数名をキーに。値を[0]=適切なパラメーター群, [1]=ラムダ関数とする。
        methods = {
            "floor": (["number"], lambda params: math.floor(params[0])),
            "nroot": (["number", "number"], lambda params: Server.nroot(params[0], params[1])),
            "reverse": (["string"], lambda params: Server.reverse(params[0])),
            "validAnagram": (["string", "string"], lambda params: Server.validAnagram(params[0], params[1])),
            "sort": (["object"], lambda params: Server.sort(params[0]))
        }

        methodName = data["method"]

        if methodName in methods:
            assert Server.validateParamsType(data["param_types"], methods[methodName][0]), "Error Occured at executing method"
            result = methods[methodName][1](data["params"])
        else:
            return json.dumps({"error": "Unknown method"})
        # あらゆる構造のデータをJSON形式にエンコーディングする→dumpsを使う
        return json.dumps(result)

    @staticmethod
    def nroot(n, x) -> float:
        return x / n
    
    @staticmethod
    def reverse(s) -> str:
        return s[::-1]
    
    @staticmethod
    def validAnagram(s, t) -> bool:
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)

    @staticmethod
    def sort(arr) -> list:
        return sorted(arr)