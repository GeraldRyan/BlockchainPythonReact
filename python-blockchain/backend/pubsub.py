import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

subscribe_key = "sub-c-551b4d2a-6b56-11eb-9994-e2667f94577d"
publish_key = "pub-c-8f40bdb7-10f0-4867-8bcc-cfd3af4a26f5"

pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key

TEST_CHANNEL = "TEST_CHANNEL"


class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f'\n-- Incoming message_object: {message_object}')


class PubSub():
    '''
    Handles the publish/subscribe layer of the application
    Provides communication between the nodes of the blockchain network.
    '''

    def __init__(self):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, channel, message):
        '''
        Publish the message object to the channel.
        '''
        self.pubnub.publish().channel(channel).message(message).sync()


def main():
    pubsub = PubSub()
    time.sleep(1)

    pubsub.publish(TEST_CHANNEL, {'foo': 'var'})


if __name__ == '__main__':
    main()
