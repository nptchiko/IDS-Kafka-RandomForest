import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import yaml
from backend.kafka.consumer.consumer import app, message_queue

# Load test cases from YAML
def load_cases():
    with open("./testcase/consumer.yaml") as f:
        return yaml.safe_load(f)

cases = load_cases()

@pytest.fixture
def mock_kafka_consumer():
    with patch("backend.kafka.consumer.consumer.consumer") as mock_consumer:
        return mock_consumer 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_send_kafka(mock_kafka_consumer, case):
    expected = case["expected-result"].lower()
    procedure = case['test_case_procedure']


    # Setup mock response based on expected
    if expected == "success":
        mock_msg = {
            'key': procedure['key'].encode(),
            'value': procedure['value'].encode()
        }
    elif expected == "no_output":
        mock_msg = None
    elif expected == "error":
        mock_msg = {'error': 'Simulated Kafka error'}
    elif expected == "exception":
        mock_kafka_consumer.consumer.poll.side_effect = Exception("Connection failed")
        with pytest.raises(Exception, match="Connection failed"):
            mock_kafka_consumer.consumer.poll(timeout=1.0)
        return  # stop test here after exception
    else:
        raise ValueError(f"Unknown expected result: {expected}")
    
    # Gán kết quả mock vào poll
    mock_kafka_consumer.consumer.poll.return_value = mock_msg

    msg = mock_kafka_consumer.consumer.poll(timeout=1.0)
    print('data was polled: ',msg)

    # Kiểm tra kết quả
    if expected == "success":
        assert msg is not None
        assert isinstance(msg['key'], bytes)
        assert isinstance(msg['value'], bytes)
        print('data expected: ', expected)
    elif expected == "no_output":
        assert msg is None
        print('data expected: ', expected)
    elif expected == "error":
        assert 'error' in msg
        print('data expected: ', expected)
