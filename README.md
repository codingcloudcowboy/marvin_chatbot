# marvin_chatbot

## Steps to run Rasa
1. Navigate to the correct directory. Train the model.

```rasa train```

2. Open up 2 Terminals. Run the Custom Actions server on one of the two.

```rasa run actions```

3. On the other terminal, run this command to access the Chatroom UI: 

```rasa run --credentials ./credentials.yml  --enable-api --auth-token XYZ123 --model ./models --endpoints ./endpoints.yml --cors "*"```

4. Afterwards, right-click html file and open it up in your browser with chrome.
