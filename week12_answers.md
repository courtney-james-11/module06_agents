# Week 12 answers

## Exercise 1
1. The messages the customer typed: I want to change my shipping address, It's order A102, and 9 Pine Street, Tampa.
2. How many tool requests were refused, and why: The 1st and 2nd request because the customer did not input the order number and new address.
3. If the customer now types "thanks", how many messages does Ollama receive on the next call? 14 messages
4. Why does "Do you sell gift cards?" still go to a person, and why is that acceptable? It still goes to a person because it looks for the handoff word 'card' anywhere in the message. Its acceptable to prevent card information from entering the model.

```(.venv) Simon-Laptop% python3 main.py
Type a message, or type quit to stop.
You: I want to change my shipping address
Sunny: Your request to change the shipping address for order A100 has been submitted and is awaiting staff approval.
You: quit
Messages in this conversation: 3
Staff review
Request 1: A100 to 123 Main St, Anytown, AN 12345
Approve? yes or no: no
Request 1 rejected.
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street
```