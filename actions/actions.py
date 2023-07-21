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
        print("ENTRA A LA FUNCION")
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
                                "id": "demo",
                                "title": "Quiero un Demo"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "adviser",
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


class ActionCreateUser(Action):
    def name(self) -> Text:
        return "action_create_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        last_name = tracker.get_slot("last_name")
        company_name = tracker.get_slot("company_name")
        email = tracker.get_slot("email")
        people_count = tracker.get_slot("people_count")
        #user_phone = tracker.sender_id
        user_phone = "+573013495690"
        # user_phone = "+573005437825"

        auth_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZX0.XkKnFaIbPwZ7CzGzVIBk_fxk4fjOTk27Xo5dGejlVbM'
        headers = {'Authorization': f'Bearer {auth_token}'}
        company_body_req = {
            "name": company_name,
        }
        # TODO: Intent convert async function
        company_response = requests.post(
            f"http://localhost:8000/organizations?email_owner={email}", json=company_body_req, headers=headers)
        
        print("COMPANY", company_response)
        
        company_response = company_response.json()

        print("COMPANY", company_response)

        user_body_req = {
            "name": name,
            "last_name": last_name,
            "email": email,
            "phone_number": user_phone,
            "role_id_fk": 1,
            "password": "doit2023",
            "organization_uid_fk": company_response["uid"]
        }

        user_response = requests.post(
            "http://localhost:8000/users", json=user_body_req, headers=headers)
        
        print("USER", user_response)

        user_response = user_response.json()
        
        print("USER", user_response)

        dispatcher.utter_message(
                text=f"Has quedado registrado, en el siguiente link https://drive.google.com/drive/folders/{company_response['drive_folder_id']} encontraras el archivo de gestion para que empieces a probar nuestra herramienta")
        return [
            SlotSet("organization", company_response),
            SlotSet("user", user_response),
            SlotSet("user_created", True), 
        ]

class ActionAskOpenFile(Action):
    def name(self) -> Text:
        return "action_ask_open_file"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("ENTRA A LA FUNCION Could open file")
        dispatcher.utter_message(json_message={"interactive": {
            "body": {
                "text": "Lograste acceder al archivo de gestión del proyecto?"
            },
            "type": "button",
            "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "si",
                                "title": "Sí 👍🏻"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "no",
                                "title": "No 👍🏻"
                            }
                        }
                    ]
            }
        }})
        return []

class ActionAskAddUsers(Action):
    def name(self) -> Text:
        return "action_ask_add_users"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("ENTRA A LA FUNCION Could add users")
        dispatcher.utter_message(json_message={"interactive": {
            "body": {
                "text": "Lograste llenar el listado de usuarios?"
            },
            "type": "button",
            "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "si",
                                "title": "Sí 👍🏻"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "no",
                                "title": "No 👍🏻"
                            }
                        }
                    ]
            }
        }})
        return []
    
class ActionAskAddTasks(Action):
    def name(self) -> Text:
        return "action_ask_add_tasks"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("ENTRA A LA FUNCION Could add tasks")
        dispatcher.utter_message(json_message={"interactive": {
            "body": {
                "text": "Lograste llenar el listado de tareas?"
            },
            "type": "button",
            "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "si",
                                "title": "Sí 👍🏻"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "no",
                                "title": "No 👍🏻"
                            }
                        }
                    ]
            }
        }})
        return []

class ValidateOnboardingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_onboarding_form"

    def validate_open_file(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `open_file` value."""
        print(f"Option given = {slot_value}")
        intent = tracker.latest_message['intent'].get('name')

        if intent == "affirm":
            return {"open_file": True}
        elif intent == "deny":
            dispatcher.utter_message(
                text="Para continuar, debes validar si lograste abrir el archivo")
            return {"open_file": None}
        else:
            dispatcher.utter_message(
                text="Disculpa, No logre entender tu respuesta")
            return {"open_file": None}
    
    def validate_add_users(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `add_users` value."""
        print(f"Option given = {slot_value}")
        intent = tracker.latest_message['intent'].get('name')

        if intent == "affirm":
            organization = tracker.get_slot("organization")[0]
            organization_id = organization['uid']
            auth_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZX0.XkKnFaIbPwZ7CzGzVIBk_fxk4fjOTk27Xo5dGejlVbM'
            headers = {'Authorization': f'Bearer {auth_token}'}
            requests.post(f"http://localhost:8000/import-users?organization_uid={organization_id}", headers=headers)
            return {"add_users": True}
        elif intent == "deny":
            dispatcher.utter_message(
                text="Para continuar, debes validar si lograste agregar usuarios")
            return {"add_users": None}
        else:
            dispatcher.utter_message(
                text="Disculpa, No logre entender tu respuesta")
            return {"add_users": None}
    
    def validate_add_tasks(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `add_tasks` value."""
        print(f"Option given = {slot_value}")
        intent = tracker.latest_message['intent'].get('name')

        if intent == "affirm":
            organization = tracker.get_slot("organization")[0]
            organization_id = organization['uid']
            auth_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZX0.XkKnFaIbPwZ7CzGzVIBk_fxk4fjOTk27Xo5dGejlVbM'
            headers = {'Authorization': f'Bearer {auth_token}'}
            requests.post(f"http://localhost:8000/import-task?organization_uid={organization_id}", headers=headers) 
            return {"add_tasks": True}
        elif intent == "deny":
            dispatcher.utter_message(
                text="Para continuar, debes validar si lograste agregar tareas")
            return {"add_tasks": None}
        else:
            dispatcher.utter_message(
                text="Disculpa, No logre entender tu respuesta")
            return {"add_tasks": None}

