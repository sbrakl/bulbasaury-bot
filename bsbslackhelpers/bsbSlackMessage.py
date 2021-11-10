# This module has some helper method to identify slack message by event payload
# Reference: https://api.slack.com/events/message

class BSB_SlackMessage:

    def __init__(self, message_event, bot_id):
        self._raw_message = message_event
        self._bot_userId = bot_id
        self._event = self.event()
        self._userId = self.user_id()


    def IsDirectMessage(self):
        event = self._event
        if not event:
            return False
        subtype = event.get('subtype', '')
        if subtype:
            #This message could be channel_join, message_deleted, pinned_item, etc
            #Find all subtypes at https://api.slack.com/events/message#subtypes
            return False
        reactions = event.get('reactions', '')
        if reactions:
            return False

        isThreadMessagebool = self.IsThreadMessage(event)
        if isThreadMessagebool:
            return False

        return True

    def event(self):
        me = self._raw_message
        event = me.get('event', {})
        return event

    def user_id(self):
        me = self._event
        user_id = me.get('user', {})
        return user_id

    def IsMessageFromBot(self):
        return self._userId == self._bot_userId


    def IsThreadMessage(self, event):
        # If message is reply to thread
        thread_ts = event.get('thread_ts', '')
        parent_user_id = event.get('parent_user_id', '')
        if thread_ts or parent_user_id:
            return True

    def HasMessageEvent(self):
        if self._event:
            return True
        else:
            return False