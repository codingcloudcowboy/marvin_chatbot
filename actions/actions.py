# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#from stock import search_stock, track_stock_price


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
