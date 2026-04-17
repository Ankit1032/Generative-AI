# P50, P95, and P99 Latency Metrics in RAG

In Retrieval-Augmented Generation (RAG), **P50**, **P95**, and **P99** are percentile-based metrics used to measure the **end-to-end response time (latency)** of the pipeline. Unlike simple averages, these percentiles reveal how performance varies across different users and requests.

## Core Metrics Defined

- **P50 (Median Latency)**: Represents the **"typical" user experience**. Exactly 50% of requests are faster than this value, and 50% are slower.
- **P95**: An early indicator of **"tail latency."** It shows the response time for 95% of requests, meaning only the slowest 5% of users experience a delay longer than this. It is a common baseline for Service Level Agreements (SLAs).
- **P99**: Represents the worst-case performance for the vast majority of users. It marks the threshold for the slowest 1% of requests. This is critical for high-scale systems where "only 1%" can still affect thousands of people.

## Latency in RAG Pipelines

RAG pipelines are uniquely sensitive to these metrics because they consist of multiple sequential steps, each adding its own latency:

1. **Preprocessing**: Embedding the user query.
2. **Retrieval**: Searching vector databases for relevant documents.
3. **Generation**: The LLM processing those documents to generate a response.

A typical production RAG system might target a **P50** of around **2.5 seconds**, while the **P95** might climb to **4 seconds**. A significant gap between P50 and P99 usually signals architectural bottlenecks like cold starts, heavy document retrieval, or LLM token limits.

## Summary Table

| Metric | User Segment       | Purpose in RAG                                      |
|--------|--------------------|-----------------------------------------------------|
| **P50**    | The "Average" User | Baseline health; helps detect broad regressions after a deployment. |
| **P95**    | 95% of Users       | Standard performance tuning; used for alerting and general user satisfaction. |
| **P99**    | The Slowest 1%     | Identifying rare outliers, such as massive document retrievals or complex reasoning. |
