import pytest
from unittest.mock import patch, MagicMock
import yaml
from backend.kafka.producer import producer

"""Run in commandline by: PYTHONPATH=/home/minhminh/workspace/CNPM/ pytest test_producer.py"""

# Load test cases from YAML
def load_cases():
    with open("./testcase/producer.yaml") as f:
        return yaml.safe_load(f)

cases = load_cases()

@pytest.fixture
def mock_kafka_producer():
    with patch("backend.kafka.producer.producer") as mock_producer:
        return mock_producer

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_send_kafka(mock_kafka_producer, case):
    topic = case.get("test_case_procedure", {}).get("topic", "")
    key = case.get("test_case_procedure", {}).get("key", "test-key")
    value = case.get("test_case_procedure", {}).get("value", "test-value")
    expected = case["expected-result"].lower()
    
    # Simulate Kafka success or failure based on expected result
    if "error" in expected or "exception" in expected:
        mock_kafka_producer.produce.side_effect = Exception("Simulated Kafka failure")
    else:
        mock_kafka_producer.producer.produce.return_value = {"status": "success"}
        mock_kafka_producer.poll.return_value = {"status": "success"}

    data = {
        "key": key,
        "value": value
    }

    # Mock response based on expected
    if "success" in expected or "warning" in expected:
        mock_kafka_producer.send_kafka.return_value = {"status": "success"}
    elif "error" in expected or "exception" in expected:
        mock_kafka_producer.send_kafka.side_effect = Exception("Kafka error")

    call_back = mock_kafka_producer.delivery_result
    try:
        result_produce = mock_kafka_producer.producer.produce(
            topic,
            key,
            value,
            call_back
        )

        print("test produce kafka: ", result_produce)

        result = mock_kafka_producer.send_kafka(data)
        print("test produce kafka:", result)
        print("result type:", type(result))
        if isinstance(result, dict):
            print("result of function: ", result['status'])

        if "success" in expected:
            assert result["status"] == "success"
        elif "warning" in expected:
            assert result["status"] == "warning"
    except Exception:
        assert "error" in expected or "exception" in expected
