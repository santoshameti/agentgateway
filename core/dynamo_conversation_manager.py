import boto3
import dotenv
from botocore.exceptions import ClientError
from typing import List, Dict, Any, Optional
import uuid, os
import json
from core.conversation_manager import ConversationManager


class DynamoConversationManager(ConversationManager):

    def __init__(self, table_name: str, region_name: str =""):
        dotenv.load_dotenv()
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        region_name = os.environ.get('AWS_REGION', 'us-west-2')  # Default to us-west-2 if not specified

        self.dynamodb = boto3.resource('dynamodb',
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=region_name
                                       )
        self.table = self.dynamodb.Table(table_name)

    def start_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        self.table.put_item(Item={
            'conversation_id': conversation_id,
            'history': json.dumps([])
        })
        return conversation_id

    def get_conversation_history(self, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        else:
            try:
                response = self.table.get_item(Key={'conversation_id': conversation_id})
                return json.loads(response['Item']['history'])
            except ClientError:
                return []

    def clear_conversation_history(self, conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        else:
            self.table.delete_item(Key={'conversation_id': conversation_id})

    def add_to_conversation_history(self, message: Dict[str, Any], conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        history = self.get_conversation_history(conversation_id)
        history.append(message)
        self.table.update_item(
            Key={'conversation_id': conversation_id},
            UpdateExpression='SET history = :val',
            ExpressionAttributeValues={':val': json.dumps(history)}
        )

    def extend_conversation_history(self, messages: List, conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        history = self.get_conversation_history(conversation_id)
        history.extend(messages)
        self.table.update_item(
            Key={'conversation_id': conversation_id},
            UpdateExpression='SET history = :val',
            ExpressionAttributeValues={':val': json.dumps(history)}
        )

    def get_formatted_conversation_history(self, conversation_id: Optional[str] = None) -> str:
        history = self.get_conversation_history(conversation_id)
        formatted_history = ""
        for message in history:
            formatted_history += f"{message['role'].capitalize()}: {message['content']}\n"
        return formatted_history.strip()