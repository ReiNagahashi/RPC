# outline
To understand the client-server model, I implemented a client in TypeScript and a server in Python. Through this learning experience, I was able to:
1. Systematically learn the necessary concepts for the client-server model, such as types of protocols, socket families, and socket types, as well as how to use them.
2. Acquire the method to implement RPC (Remote Procedure Call) using the client-server model. This allows the client to send requests to the server and use functions prepared on the server.

## The following were actually used:
- Protocol: UDP
- Socket Family: AF_INET
- Socket Type: SOCK_DGRAM

## Functions implemented on the server:

- `floor(double x)`: Rounds down the decimal number x to the nearest integer and returns the result as an integer.
- `nroot(int n, int x)`: Calculates the value of r in the equation rn = x.
- `reverse(string s)`: Takes a string s as input and returns a new string that is the reverse of the input string.
- `validAnagram(string str1, string str2)`: Takes two strings as input and returns a boolean indicating whether the two input strings are anagrams of each other.
- `sort(string[] strArr)`: Takes an array of strings as input, sorts the array, and returns the sorted array of strings.

## Note
In the first commit, I implemented a simple message exchange on the CLI to ensure that the client and server, written in different languages, could communicate properly. In subsequent commits, I committed functions for implementing RPC (Remote Procedure Call) and fixes for bugs in those functions.
