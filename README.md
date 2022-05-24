# Chatbot
chatbot that answers the questions about planets in our solar system
 
This application is able to answer on user´s questions related to one of the 8 planets in our solar system. After the app is opened, there will be printed one of the greets with question, about which planet the user wants to speak. User should specify a name of planet in the response - otherwise bot will print warning that he does not understand. 
If the planet is specified, bot will ask, in what is user interested in about specified planet. When user answer this question, bot will print out the result. If bot does not understand the question, it will print sentence that guide user to ask something different:

![image](https://user-images.githubusercontent.com/76043407/170072219-831db61c-c652-40cf-b0ee-bdd3497a19af.png)

The bot throws correct answer according to the highest cosine similarity between vectors in TF-IDF matrix. one of those vectors is user´s question, other one is one of the texts scraped from website with informations about planets. Before the TF-IDF matrix is made from text data, these texts are processed by NLP techniques.
