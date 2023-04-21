import requests
from datetime import date
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import SlotSet, ActionExecuted, UserUttered
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ActionAskAcceptedDataPolicy(Action):
    def name(self) -> Text:
        return "action_ask_accepted_data_policy"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(json_message={"interactive": {
            "body": {
                "text": "Es importante para nosotros que leas y aceptes el tratamiento que hacemos con tus datos \nhttps://www.doit.care/data-policy \n Debes saber que para contunuar debes aceptar 😁"
            },
            "type": "button",
            "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "si",
                                "title": "Acepto 👍🏻"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "no",
                                "title": "No acepto 👍🏻"
                            }
                        }
                    ]
            }
        }})
        return []

class ValidateDataPolicyForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_data_policy_form"

    def validate_accepted_data_policy(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `accepted_data_policy` value."""
        print(f"Option given = {slot_value}")
        intent = tracker.latest_message['intent'].get('name')

        if intent == "affirm":
            return {"accepted_data_policy": True}
        elif intent == "deny":
            dispatcher.utter_message(
                text="Entendemos, desafortunadamente para continuar la conversación debes aceptar el tratamiento de datos. Esperamos tengas un excelente dia")
            return {"accepted_data_policy": False}
        else:
            dispatcher.utter_message(
                text="Disculpa, No logre entender tu respuesta")
            return {"accepted_data_policy": None}

class ActionAskMainOption(Action):
    def name(self) -> Text:
        return "action_ask_main_option"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(json_message={"interactive": {
            "body": {
                "text": "Cuentanos que como podemos colaborarte hoy?"
            },
            "type": "button",
            "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "si",
                                "title": "Quiero un Demo"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "no",
                                "title": "Hablar con un asesor"
                            }
                        }
                    ]
            }
        }})
        return []

class ValidateMainMenuForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_main_menu_form"

    def validate_main_option(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `main_option` value."""
        print(f"Option given = {slot_value}")
        MAIN_OPTIONS = ["demo", "adviser"]

        if slot_value in MAIN_OPTIONS:
            return {"main_option": slot_value}
        else:
            dispatcher.utter_message(
                text="Disculpa, No logre entender tu respuesta")
            return {"main_option": None}

class ValidateUserForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""
        print(f"Option given = {slot_value}")

        if len(slot_value) > 3:
            return {"name": slot_value}
        else:
            dispatcher.utter_message(
                text="Disculpa, por favor indacanos tu nombre")
            return {"name": None}
    
    def validate_company_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `company_name` value."""
        print(f"Option given = {slot_value}")

        if len(slot_value) > 3:
            return {"company_name": slot_value}
        else:
            dispatcher.utter_message(
                text="Disculpa, por favor indacanos el nombre de tu empresa")
            return {"company_name": None}
    
    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email` value."""
        print(f"Option given = {slot_value}")

        if len(slot_value) > 3:
            return {"email": slot_value}
        else:
            dispatcher.utter_message(
                text="Disculpa, por favor indacanos un email valido")
            return {"email": None}
    
    def validate_people_count(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `people_count` value."""
        print(f"Option given = {slot_value}")

        if len(slot_value) > 3:
            return {"people_count": slot_value}
        else:
            dispatcher.utter_message(
                text="Disculpa, por favor indacanos un número")
            return {"people_count": None}