# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#from stock import search_stock, track_stock_price

#azure sms funtion
import os
from azure.communication.sms import SmsClient
# Create the SmsClient object which will be used to send SMS messages, also authenticates to azure
sms_client = SmsClient.from_connection_string('endpoint=https://armtexttest.communication.azure.com/;accesskey=5EMxfFuvkAoVA77e1U1eG9w8SJwBKAgXID1r7fIiLWk1rEfTcxMY9wWYs/ysRFD+a3bDjz9YhrfkJ8cnCymR/g==')
########
def send_text(tel_number, text):
    sms_responses = sms_client.send(
    from_="+18334821558", # has to be this number, it has been purchased
    # to=["+12103820029", "+12103834324", "+19728375227"], #this is how you do multiple numbers
    to=tel_number,
    message=text
    ) # optional property

####
#send_text('+14693867024', "This is sunday")



class ActionMedication(Action):

     def name(self) -> Text:
         return "action_medication"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Did you take your medications?")

         return []


class ActionMedicationReminder(Action):

    def name(self) -> Text:
        return "action_medication_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Please take your meds!")

        return []


class ActionStocks(Action):

    def name(self) -> Text:
        return "action_check_stocks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='What stock do you want to track?')
        #respond('Hello')
        
        return []

class TrackStocks(Action):

    def name(self) -> Text:
        return "action_track_stocks"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            stockVar = tracker.latest_message['text']
            message = self.search_stock(stockVar)
            dispatcher.utter_message(text=message)
            dispatcher.utter_message(text='What price to track?')
            
    def search_stock(self, search_term):
        import time
        import yfinance as yf # to fetch financial data

        stocks = {
                "apple":"AAPL",
                "facebook":"FB",
                "tesla":"TSLA",
            }
            
        try: 
            stock = stocks[search_term]
            stock = yf.Ticker(stock)
            price = stock.info["regularMarketPrice"] 
            #send text
            send_text('+15126589792', "'The price of '+str(search_term)+' is '+str(price)+' '+str(stock.info["currency"])")
            return 'The price of '+str(search_term)+' is '+str(price)+' '+str(stock.info["currency"])

        except:
            return 'oops, something went wrong'
            
class NotifyStockPrice(Action):

    def name(self) -> Text:
        return "action_notify_stock_price"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            price = tracker.latest_message['text']
            userEvents = []
            for event in tracker.events:
                if event.get("event") == "user":
                    userEvents.append(event)
            print(userEvents)
            stockVar = userEvents[len(userEvents)-2]['text']
            
            message = self.track_stock_price(stockVar, price)
            dispatcher.utter_message(text=message)   
           
    def track_stock_price(self, search_term, search_price):
        import time
        import yfinance as yf # to fetch financial data
        
        stocks = {
                "apple":"AAPL",
                "facebook":"FB",
                "tesla":"TSLA",
            }
        
        stock = stocks[search_term]
        stock = yf.Ticker(stock)
        price = stock.info["regularMarketPrice"]
     
        if price < int(search_price):
            return 'Price hit!'
            
        else:
            return 'I have set a reminder for '+search_term+' at '+search_price+' '+stock.info["currency"]
