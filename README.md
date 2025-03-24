# prometheus-summary
Prometheus summary with quantiles over configurable sliding time window

## Installation

```
pip install prometheus-summary==0.1.5
```
This package can be found on [PyPI](https://pypi.org/project/prometheus-summary/).

## Documentation
Documentation is available on https://prometheus-summary.readthedocs.io/en/latest/.

## Collecting

### Basic usage

```python
from prometheus_summary import Summary

s = Summary("request_latency_seconds", "Description of summary")
s.observe(4.7)
```

### Usage with labels

```python
from prometheus_summary import Summary

s = Summary("request_latency_seconds", "Description of summary", ["method", "endpoint"])
s.labels(method="GET", endpoint="/profile").observe(1.2)
s.labels(method="POST", endpoint="/login").observe(3.4)
```

### Usage with custom quantiles and precisions

By default, metrics are observed for the following (quantile, precision (inaccuracy)) pairs:

`((0.50, 0.05), (0.90, 0.01), (0.99, 0.001))`

You can also provide your own values when creating the metric.

```python
from prometheus_summary import Summary

s = Summary(
    "request_latency_seconds", "Description of summary",
    invariants=((0.50, 0.05), (0.75, 0.02), (0.90, 0.01), (0.95, 0.005), (0.99, 0.001)),
)
s.observe(4.7)
```

### Usage with custom time window settings

Typically, you don't want to have a Summary representing the entire runtime of the application,
but you want to look at a reasonable time interval. This Summary metric implement a configurable sliding time window.

The default is a time window of 10 minutes and 5 age buckets, i.e. the time window is 10 minutes wide, and
we slide it forward every 10 / 5 = 2 minutes, but you can configure this values for your own purposes.

```python
from prometheus_summary import Summary

s = Summary(
    "request_latency_seconds", "Description of summary",
    # time window 5 minutes wide with 10 age buckets (sliding every 30 seconds)
    max_age_seconds=5 * 60,
    age_buckets=10,
)
s.observe(4.7)
```

## Querying

Suppose we have a metric:

```python
from prometheus_summary import Summary

s = Summary("request_latency_seconds", "Description of summary", ["method", "endpoint"])
```

To show request latency by `method`, `endpoint` and `quantile` use the following PromQL query:
```
max by (method, endpoint, quantile) (request_latency_seconds)
```

To show only 99-th quantile:
```
max by (method, endpoint) (request_latency_seconds{quantile="0.99"})
```
