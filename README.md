# blockchain-med-integrity

## Ensuring patient data integrity using Blockchain
For our tests, we use a local version of the Ethereum blockchain. This can be provided by Ganache. In our case, for purpose of visualization we installed the GUI version (instead of maybe having the CLI version). The following screenshot shows our contract creation transaction on the blockchain.

![Contract deployed on Ganache](https://user-images.githubusercontent.com/28572130/118322543-95557d00-b4ff-11eb-8757-40f4ec6afa53.png)


We developed an API, which will act as an application (basically without a frontend), through which physician for instance can modify or retrieve patients data. On the following screenshot we show a successful modification of the data of one patient

![1](https://user-images.githubusercontent.com/28572130/118322630-bf0ea400-b4ff-11eb-8d40-133377f9fb08.png)


This is repercussed on the blockchain as a new transaction happened. In fact, when the patient data is modified, a hash version of this data is stored on the blockchain.

![Screenshot from 2021-05-14 18-33-37](https://user-images.githubusercontent.com/28572130/118322675-cd5cc000-b4ff-11eb-9fb3-b546c0c74c72.png)


Now, let's imagine that an attacker gets a direct access to our database by an unknown means and decide to alter patient data (the following screenshot shows data tampering with Robot3T knowing that our data is stored in a MongoDB database). Let's say for instance the attacker wants to undermine a patient reputation. In order to do so, he decides to reflect in the DB that the given patient has AIDS. It goes as follow:

![2](https://user-images.githubusercontent.com/28572130/118322657-c766df00-b4ff-11eb-9d63-7183c03c3ee5.png)


With our developed system, patient data integrity is ensured so that when a physician for instance wants to retrieve the data he/she will get an alert of data integrity issue. The admin of the system will receive an email as shown on the following screenshot. He will be alerted in the case that a patient data integrity has been compromised

![kZJPOz](https://user-images.githubusercontent.com/28572130/118322813-0432d600-b500-11eb-82a6-717c96e38fb5.jpeg)

It is a bit useless to have an alert without actually doing anything to have consistent data. So, we decide to revert the information back from a backup database. In real situation, the backup database should be on another server. When this process is done, the physician will receive the information as follow:

![3](https://user-images.githubusercontent.com/28572130/118322665-c9c93900-b4ff-11eb-9846-bef76a39c60e.png)

To be even more effective, a system of this kind should maybe include daily integrity check to limit the time an attacker could spend in a system without being caught
