---
layout: single
title: "What Counts as Streaming? File Triggers, Micro-Batches, and the 1 Minute Question"
date: 2026-05-22 09:00:00 +0000
categories: [data-engineering]
excerpt: "A practical definition of streaming in modern data systems, including file-triggered jobs and one-minute micro-batches."
---

A question I hear all the time is this: if I process new files every minute, is that really streaming?

Short answer: yes, in most modern data platforms that is still streaming. It is usually called micro-batch streaming.

## Streaming is about continuous ingestion intent

In practice, streaming means your pipeline is designed to process incoming data continuously over time, not in large scheduled historical chunks.

That can happen in different ways:

- Event by event processing
- Small micro-batches every few seconds or minutes
- File arrival triggers that process new files as they land

All three can be valid streaming patterns depending on latency needs.

## File based trigger streams are still streams

In Spark Structured Streaming and Databricks Auto Loader style patterns, new files are detected and processed incrementally. Even if input arrives as files, the engine tracks offsets and state over time.

That is very different from a daily batch that rescans a full folder and recomputes everything.

## Is 1 minute micro-batching streaming?

Usually yes.

A one minute trigger gives near real time behavior for many business cases:

- Operational dashboards
- Alerting with modest SLA requirements
- Incremental feature refreshes
- Data products where sub second latency is not required

If your stakeholders need updates in under five seconds, one minute may be too slow. But that is a latency decision, not a definition problem.

## A practical way to classify pipelines

I like this simple split:

1. **Batch**: finite historical window, explicit run boundaries, often full or large incremental recompute.
2. **Streaming (micro-batch)**: unbounded input, frequent trigger intervals, persistent checkpoint and state.
3. **Streaming (continuous/event)**: record level or ultra low latency processing.

Most production data teams live in the middle category because it balances reliability, cost, and freshness.

## What matters more than labels

Instead of arguing about vocabulary, lock in these design questions:

- What is the required end to end latency?
- What is acceptable data loss risk?
- How will checkpointing and replay work?
- How do we handle schema evolution?
- What happens when source volume spikes?

If those answers are solid, your architecture is probably in good shape whether your trigger is every 5 seconds or every 1 minute.

For most data engineering teams, micro-batching is not a compromise. It is the practical center of gravity.
