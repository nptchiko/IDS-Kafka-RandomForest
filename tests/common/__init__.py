from confluent_kafka import Consumer
import os

_GROUP_PROTOCOL_ENV = 'TEST_CONSUMER_GROUP_PROTOCOL'

class TestUtils:
    @staticmethod
    def broker_version():
        return '5.3.0'
    
    @staticmethod
    def broker_conf():
        broker_conf = ['transaction.state.log.replication.factor=1',
                       'transaction.state.log.min.isr=1']
    
    @staticmethod
    def use_group_protocol_consumer():
        return _GROUP_PROTOCOL_ENV in os.environ and os.environ[_GROUP_PROTOCOL_ENV] == 'consumer'

class TestConsumer(Consumer):
    def __init__(self, conf=None, **kwargs):
        return None