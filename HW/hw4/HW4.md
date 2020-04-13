#  CSE224 HW4

##### Yawen Zhao A53280596

### Provisioning virtual machines

Leader

![Screen Shot 2019-11-18 at 9.55.52 PM](/Users/yawen_zhao/Desktop/Screen Shot 2019-11-18 at 9.55.52 PM.png)

Follower

![Screen Shot 2019-11-18 at 9.56.06 PM](/Users/yawen_zhao/Desktop/Screen Shot 2019-11-18 at 9.56.06 PM.png)

Above are the two instance I created. One in Oregon. One in Seoul.



### Performing basic benchmarking

![Screen Shot 2019-11-18 at 9.53.30 PM](/Users/yawen_zhao/Desktop/Screen Shot 2019-11-18 at 9.53.30 PM.png)


The RTT I measure is averagely 126.223ms, which is shown as above. 

The distance between Seoul and Oregon is 8697km. Given the speed of light in fiber-optic cable which is equal to 2/3 of the speed of light in vaccum, the RTT can be computed as 

​                                             $$8697\:km \times 2 / (3.0\times10^5\:km/s \times 2/3)=86.97\:ms$$



#### Benchmarking Kafka

![Screen Shot 2019-11-18 at 11.29.02 PM](/Users/yawen_zhao/Desktop/Screen Shot 2019-11-18 at 11.29.02 PM.png)

The mean half RTT calculted by Kafka is 68.3 ms. So the RTT is approximately 136.6ms. 

The result is a little bit larger than the result meatured by ping method, which may cause by the inconsistent of the clock of the two machine.

Below are the code of producer and consumer:

producer.py

![Screen Shot 2019-11-18 at 11.38.33 PM](/Users/yawen_zhao/Desktop/Screen Shot 2019-11-18 at 11.38.33 PM.png)

consumer.py

![Screen Shot 2019-11-18 at 11.38.33 PM](/Users/yawen_zhao/Desktop/Screen Shot 2019-11-18 at 11.38.33 PM.png)