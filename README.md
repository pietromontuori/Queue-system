# Queue-system
This is a queue system i developed in python for a 4th year subject in the university. This were the requirements:

What is the quantity of each product sold after 8 hours in a fast food drive-thru with exponential inter-arrival time (5 cars every 10 minutes)? All customers form a single line and are served in order of arrival. Each car places an order and waits until it is delivered before the next is attended to.

20% of customers order a family lunch, while 50% order a simple lunch, and the remaining 30% order a super ice cream dessert. 50% of cars order 1 unit of the product, 30% order 2, and 20% order 3 (always of the same type). The quantity of the order, called x, is used to calculate the preparation delay, with the following times: 5 - (3/x) constant minutes for family lunch, N(2,1) * x minutes for a simple lunch, and U(1,2) minutes for the super ice cream dessert (the quantity of units does not affect the delay).

The delivery time has a normal distribution N(30,15) seconds regardless of the product requested. Cars do not join the queue if there are already four waiting. Additionally, the abandonment time of the queue is 8 minutes.
