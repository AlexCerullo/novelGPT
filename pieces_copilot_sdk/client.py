import openai
from dotenv import load_dotenv
import os

#Load env var from api.env
load_dotenv('api.env')
api_key = os.getenv('OPENAI_API_KEY')

openai.api_key = api_key

class PiecesClient:
    def __init__(self, config: dict):
        self.api_key = config.get('apiKey', api_key)
        openai.api_key = self.api_key

    def ask_question(self, question: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Be extremely sassy!"},
                    {"role": "user", "content": question},
                ]
            )
            answer_text = response['choices'][0]['message']['content'].strip()
            return answer_text
        except Exception as error:
            print(f'Error asking question: {error}')
            return 'Error asking question'

    def create_conversation(self, props: dict = None) -> dict:
        if props is None:
            props = {}

        first_message = props.get('firstMessage', 'Hello!')
        response = self.ask_question(first_message)
        return {'conversation_id': 'local-conversation-id', 'answer': response}

    def prompt_conversation(self, message: str, conversation_id: str) -> dict:
        try:
            response = self.ask_question(message)
            return {'text': response}
        except Exception as error:
            print(f'Error prompting conversation: {error}')
            return {'text': 'Error asking question'}

    def create_conversation(self, props: dict = None) -> dict:
        if props is None:
            props = {}

        name = props.get('name', 'New Conversation')
        first_message = props.get('firstMessage')

        try:
            new_conversation = self.conversations_api.conversations_create_specific_conversation(
                seeded_conversation={
                    'name': name,
                    # 'type': ConversationTypeEnum.Copilot,
                    'type': 'COPILOT',
                }
            )

            if first_message:
                answer = self.prompt_conversation(
                    message=first_message,
                    conversation_id=new_conversation.id,
                )

                return {
                    'conversation': new_conversation,
                    'answer': answer
                }

            return {'conversation': new_conversation}
        except Exception as error:
            print(f'Error creating conversation: {error}')
            return None

    def ask_question(self, question: str) -> str:
        try:
            answer = self.qgpt_api.question(
                qgpt_question_input={
                    'query': question,
                    'pipeline': {
                        'conversation': {
                            'generalizedCodeDialog': {},
                            'contextualizedSassyDialog': {
                                'instruction': 'Be extremely sassy!',
                            },
                        },
                    },
                    'relevant': {
                        'iterable': [],
                    }
                }
            )
            # Clean up any unwanted markdown or plaintext tags
            answer_text = answer.answers.iterable[0].text.strip('```plaintext').strip('```').strip()
            return answer_text
        except Exception as error:
            print(f'Error asking question: {error}')
            return 'Error asking question'

    def prompt_conversation(self, message: str, conversation_id: str, regenerate_conversation_name: bool = False) -> dict:
        try:
            conversation = self.get_conversation(
                conversation_id=conversation_id,
                include_raw_messages=True,
            )

            if not conversation:
                return {'text': 'Conversation not found'}

            user_message = self.conversation_messages_api.messages_create_specific_message(
                seeded_conversation_message={
                    # 'role': QGPTConversationMessageRoleEnum.User,
                    'role': 'USER',
                    'fragment': {
                        'string': {
                            'raw': message,
                        },
                    },
                    'conversation': {'id': conversation_id},
                }
            )

            relevant_conversation_messages = [
                {
                    'seed': {
                        # 'type': SeedTypeEnum.Asset,
                        'type': 'SEEDED_ASSET',
                        'asset': {
                            'application': PiecesClient.application_to_dict(self.tracked_application),
                            'format': {
                                'fragment': {
                                    'string': {
                                        'raw': msg['message'],
                                    },
                                },
                            },
                        },
                    }
                }
                for msg in (conversation.get('raw_messages') or [])
            ]

            answer = self.qgpt_api.question(
                qgpt_question_input={
                    'query': message,
                    'pipeline': {
                        'conversation': {
                            'contextualizedCodeDialog': {},
                        },
                    },
                    'relevant': {
                        'iterable': relevant_conversation_messages,
                    },
                }
            )

            bot_message = self.conversation_messages_api.messages_create_specific_message(
                seeded_conversation_message={
                    # 'role': QGPTConversationMessageRoleEnum.Assistant,
                    'role': 'ASSISTANT',
                    'fragment': {
                        'string': {
                            'raw': answer.answers.iterable[0].text,
                        },
                    },
                    'conversation': {'id': conversation_id},
                }
            )

            if regenerate_conversation_name:
                self.update_conversation_name(conversation_id=conversation_id)

            return {
                'text': answer.answers.iterable[0].text,
                'user_message_id': user_message.id,
                'bot_message_id': bot_message.id,
            }
        except Exception as error:
            print(f'Error prompting conversation: {error}')
            return {'text': 'Error asking question'}