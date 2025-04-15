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
    with patch("backend.kafka.producer") as mock_producer:
        return mock_producer

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_send_kafka(mock_kafka_producer, case):
    expected = case["expected-result"].lower()
    
    # Simulate Kafka success or failure based on expected result
    if "error" in expected or "exception" in expected:
        mock_kafka_producer.produce.side_effect = Exception("Simulated Kafka failure")
    else:
        mock_kafka_producer.produce.return_value = None
        mock_kafka_producer.poll.return_value = None

    # Dummy input based on YAML case
    data = {
        "key": case.get("test_case_procedure", {}).get("key", "test-key"),
        "value": case.get("test_case_procedure", {}).get("value", "test-value")
    }

    try:
        result = producer.send_kafka(data)
        print("result of function: ",result['status'])
        if "success" in expected or "warning" in expected:
            assert result["status"] == "success"
    except Exception:
        assert "error" in expected or "exception" in expected
