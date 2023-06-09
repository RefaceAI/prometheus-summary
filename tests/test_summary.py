import random

import pytest
from prometheus_client import CollectorRegistry

from prometheus_summary import Summary

from prometheus_client.exposition import generate_latest


@pytest.fixture()
def registry():
    return CollectorRegistry()


@pytest.fixture()
def summary(registry):
    return Summary("test", "test", ["key"], registry=registry)


@pytest.mark.parametrize("num_observations", [1, 10, 100, 1000, 10000, 100000])
def test_random_observations(num_observations, summary, registry):
    labels = {"key": "value"}
    sum_observations = 0
    for _ in range(num_observations):
        value = random.randint(1, 1000) / 100
        summary.labels(**labels).observe(value)
        sum_observations += value

    metric_value = {}
    prometheus_response = generate_latest(registry).decode()
    for line in prometheus_response.split("\n"):
        if line and not line.startswith("#"):
            key, value = line.split(" ")
            metric_value[key] = float(value)

    assert metric_value['test_count{key="value"}'] == num_observations
    assert metric_value['test_sum{key="value"}'] == sum_observations
    assert (
        metric_value['test{key="value",quantile="0.5"}']
        <= metric_value['test{key="value",quantile="0.9"}']
        <= metric_value['test{key="value",quantile="0.99"}']
    )
