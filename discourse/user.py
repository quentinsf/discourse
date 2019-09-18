from .jsonobject import JsonObject
from .private_message import PrivateMessage
from .notification import Notification


class User(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def update_avatar(self, upload_id, type):
        response = self.client._request(
            'PUT',
            'users/{}/preferences/avatar/pick'.format(self.username),
            params={'upload_id': upload_id, 'type': type}
        )

        # TODO: Update instance attribute for avatar on success
        if response['success'] == 'OK':
            return True
        return False

    def update_email(self, email):
        response = self.client._request(
            'PUT',
            'users/{}/preferences/email'.format(self.username),
            params={'email': email}
        )

        # TODO: Documentation unclear on response, investigate
        if response['success'] == 'OK':
            return True
        return False

    def delete(
        self,
        delete_posts=False,
        block_email=False,
        block_urls=False,
        block_ip=False,
    ):
        response = self.client._request(
            'DELETE',
            'admin/users/{}.json'.format(self.id),
            params={
                'delete_posts': delete_posts,
                'block_email': block_email,
                'block_urls': block_urls,
                'block_ip': block_ip,
            }
        )

        if response['deleted'] == 'true':
            return True
        return False

    def log_out(self):
        response = self.client._request(
            'POST',
            'admin/users/{}/log_out'.format(self.id),
        )

        if response['success'] == 'OK':
            return True
        return False

    def refresh_gravatar(self):
        return self.client._request(
            'POST',
            'user_avatar/{}/refresh_gravatar.json'.format(self.username),
        )

    def get_actions(self, offset, filter):
        # TODO: Create "Action" class
        return self.client._request(
            'GET',
            'user_actions.json',
            params={
                'offset': offset,
                'username': self.username,
                'filter': filter,
            }
        )

    def get_private_messages(self):
        response = self.client._request(
            'GET',
            'topics/private-messages/{}.json'.format(self.username),
        )

        return [
            PrivateMessage(client=self, json=private_message)
            for private_message
            in response['topic_list']['topics']
        ]

    def get_private_messages_sent(self):
        response = self.client._request(
            'GET',
            'topics/private-messages-sent/{}.json'.format(self.username),
        )

        return [
            PrivateMessage(client=self, json=private_message)
            for private_message
            in response['topic_list']['topics']
        ]

    def get_notifications(self):
        response = self.client._request('GET', 'notifications.json', params={
            'username': self.username
        })

        return [
            Notification(client=self, json=notification)
            for notification
            in response['notifications']
        ]

    def mark_notifications_read(self):
        # Not well documented in API. Need to reverse-engineer
        return NotImplementedError
