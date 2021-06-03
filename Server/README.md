# Server
A realtime server for handling incoming traffic about logging, new messages and other things.

## Requirements
All requirements files are places inside `requirements.txt` file in root folder.

## Running
To run the application API must be up and running. Also the forgot password API should be run separatly. To get acces from clients an server application must be run. 

### Forgot password API 
`python Server/src/forgotPassword/forgotPassword.py`

API working port is 5050 and runs on all interfaces. Connection to this is secured using HTTPS with a self signed certificate so don't be scared by the security monit in browser. 

### TCP Server
`python Server/src/server.py`

Running on all interfaces and port 7777. Connection is using a certificate file inside a folder making is secured using TLS/SSL.

## Protocol informations
To implement connection between client and server was used a simple schema for sending data throuout a encrypted TCP stream. Header of this protocol are send inside encrypted data making it application data.

### Header
Header contains informations about used version, the type of the message and a size of the data coming right after.

<table>
    <tr>
        <th>Version</th>
        <th>Type</th>
        <th>Data size</th>
    </tr>
    <tr>
        <td>2 bits</td>
        <td>6 bits</td>
        <td>16 bits</td>
    </tr>
</table>

#### Version
Currently version of the protocol is 1, binary encoded setting it to `01` in the header.

#### Type
It specifies the fields contained inside data that is send after the header. All of them are described inside `protocol.py` file.

#### Data size
It is made up from the converted to bytes data before sending.

### Data
Bytes inside are encoded json documents which after decoding can contain specific fields based on the header type value. The header types and values are describled by the table below:

<table>
    <tr>
        <th>Header Type</th>
        <th>Required Fields</th>
        <th>Optional Fields</th>
        <th>Descrieption</th>
    </tr>
    <tr>
        <td>ACK</td>
        <td></td>
        <td><code>msg: str</code></td>
        <td>Acknowledment, for information about correct data in specific types</td>
    </tr>
    <tr>
        <td>ERR</td>
        <td></td>
        <td><code>msg: str</code></td>
        <td>Any type of error that ocured based on the recived data</td>
    </tr>
    <tr>
        <td>DIS</td>
        <td></td>
        <td><code>msg: str</code></td>
        <td>A disconnect message</td>
    </tr>
    <tr>
        <td>MSG</td>
        <td><code>reciever: str</code></td>
        <td><code>msg: str</code></td>
        <td>Message that was send</td>
    </tr>
    <tr>
        <td>LOG</td>
        <td><code>login: str</code><br><code>password: str</code></td>
        <td></td>
        <td>Login data for verifying the users</td>
    </tr>
    <tr>
        <td>SES</td>
        <td><code>session: int</code></td>
        <td></td>
        <td>Session id, send after succesfull login</td>
    </tr>
    <tr>
        <td>REG</td>
        <td><code>login: str</code><br><code>password: str</code><br><code>email: str</code></td>
        <td></td>
        <td>Register data for creating new accounts</td>
    </tr>
    <tr>
        <td>LIS</td>
        <td><code>users: list</code></td>
        <td></td>
        <td>A list of all registered users</td>
    </tr>
    <tr>
        <td>FRP</td>
        <td><code>login: str</code></td>
        <td></td>
        <td>Forgot password, which informs to send a mail to the user address</td>
    </tr>
    <tr>
        <td>HIS</td>
        <td><code>history: list</code></td>
        <td></td>
        <td>History of the current active user we are speaking to</td>
    </tr>
    <tr>
        <td>UPD</td>
        <td></td>
        <td><code>reciever: str</code></td>
        <td>Information about current user that we speak to</td>
    </tr>
    <tr>
        <td>CHP</td>
        <td><code>password: str</code></td>
        <td></td>
        <td>Change password, for logged users</td>
    </tr>
    <tr>
        <td>CHM</td>
        <td><code>email: str</code></td>
        <td></td>
        <td>Mail changing, for logged users</td>
    </tr>
    <tr>
        <td>DEL</td>
        <td></td>
        <td><code>msg: str</code></td>
        <td>Removal of the user account, only for logged users</td>
    </tr>
</table>