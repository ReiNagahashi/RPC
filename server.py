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
        

    def bind(self):
        self.socket.bind(self.address)


    def parseToDict(self, data):
        # バイトデータを文字列に変換
        jsonString = data.decode('utf-8')
        # 文字列データをディクショナリに変換
        try:
            dataDict = json.loads(jsonString)
            return dataDict

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        

    def receiveRequest(self):
        while True:
            print('\nwaiting to recieve massege')
            data, address = self.socket.recvfrom(self.maximumDataSize)
            # JSONデータを受け取るので、JSオブジェクトにパースする必要がある
            dictData = self.parseToDict(data)
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


    def validateParamsType(self, paramTypes, expectedParamTypes):
        if len(paramTypes) != len(expectedParamTypes): return False 
        for paramT, expect in zip(paramTypes, expectedParamTypes):
            if paramT != expect: return False
        return True


    def createResponse(self, data):
        # floor(double x): 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
        # nroot(int n, int x): 方程式 rn = x における、r の値を計算する。
        # reverse(string s): 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
        # validAnagram(string str1, string str2): 2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
        # sort(string[] strArr): 文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。
        methodName = data["method"]
        result = None

        if methodName == "floor":
            assert self.validateParamsType(data["param_types"], ["number"]), "Error Occured at executing method"
            result = math.floor(data["params"][0])
        elif methodName == "nroot":
            assert self.validateParamsType(data["param_types"], ["number", "number"]), "Error Occured at executing method"
            result = self.nroot(data["params"][0], data["params"][1])
        elif methodName == "reverse":
            assert self.validateParamsType(data["param_types"], ["string"]), "Error Occured at executing method"
            result = self.reverse(data["params"][0])
        elif methodName == "validAnagram":
            assert self.validateParamsType(data["param_types"], ["string", "string"]), "Error Occured at executing method"
            result = self.validAnagram(data["params"][0], data["params"][1])
        elif methodName == "sort":
            assert self.validateParamsType(data["param_types"], ["object"]), "Error Occured at executing method"
            result = self.sort(data["params"][0])
        # あらゆる構造のデータをJSON形式にエンコーディングする→dumpsを使う
        return json.dumps(result)

    def nroot(self, n, x):
        return x / n
    

    def reverse(self, s):
        return s[::-1]
    

    def validAnagram(self, s, t):
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)


    def sort(self, arr):
        return sorted(arr)