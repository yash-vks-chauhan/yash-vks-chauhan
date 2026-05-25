# Yash Chauhan

I build full-stack AI systems with an emphasis on trust, observability, and real-world operation.

Right now I am building [GlassBox](https://github.com/yash-vks-chauhan/Glassbox), an auditable wealth-advisory AI agent that answers from cited sources, refuses unsupported questions, records every decision, and exposes trust metrics through a governance dashboard.

## Current Direction

Most AI demos stop at "the model answered." I am more interested in the layer around the model:

- What evidence did it use?
- Which claims were verified or rejected?
- When should it refuse instead of guessing?
- Can an operator replay the full decision later?
- Does the system degrade safely when the model path fails?

That is the engineering thread across my recent work: AI systems that are useful, inspectable, and operationally defensible.

## Selected Projects

### [GlassBox](https://github.com/yash-vks-chauhan/Glassbox)

An auditable AI agent for regulated finance workflows.

It combines retrieval, grounded answering, claim verification, refusal routing, audit replay, determinism checks, and trust scoring. The goal is not just to answer advisor questions, but to make every answer defensible.

`Python` `FastAPI` `Next.js` `TypeScript` `scikit-learn` `PostgreSQL`

### [Autoscaler](https://github.com/yash-vks-chauhan/Autoscaler)

A local-first Kubernetes auto-healing and observability platform.

It watches live service metrics, detects anomalies, reasons about incidents, injects controlled failures, and executes Kubernetes-native recovery actions with fallback ML when external model providers are unavailable.

`Kubernetes` `NestJS` `FastAPI` `Prometheus` `TimescaleDB` `Next.js`

### [CT-Denoising-U-Net](https://github.com/yash-vks-chauhan/CT-Denoising-U-Net)

A medical image denoising pipeline for CT and X-ray scans.

It includes preprocessing, U-Net training, CLI inference, Streamlit inspection, and image-quality evaluation with metrics such as PSNR, SSIM, and MSE.

`Python` `TensorFlow` `U-Net` `Streamlit` `Jupyter`

### [KalaKraft](https://github.com/yash-vks-chauhan/Kalakraftdev)

A full-stack e-commerce platform for art products.

It includes storefront flows, authentication, admin workflows, product management, order handling, analytics, real-time features, and a polished customer experience.

`Next.js` `TypeScript` `Prisma` `PostgreSQL` `Firebase Auth`

## Technical Range

| Area | Working With |
| --- | --- |
| AI systems | RAG, grounded generation, refusal logic, evaluation gates, fallback classifiers |
| Backend | FastAPI, NestJS, REST APIs, WebSockets, auth, rate limits, structured logging |
| Frontend | Next.js, React, TypeScript, Tailwind, Recharts, operator dashboards |
| Data | PostgreSQL, TimescaleDB, vector stores, audit trails, replayable traces |
| ML | scikit-learn, TensorFlow, U-Net, anomaly detection, model-quality metrics |
| Infrastructure | Docker, Kubernetes, Prometheus, AWS-oriented deployment |

## What I Care About

I like systems where the hard part is not hidden in a prompt. Good engineering shows up in the surrounding contracts: data flow, failure behavior, observability, evaluation, security boundaries, and whether another person can understand the system after it has made a decision.

## GitHub

Browse my work here: [@yash-vks-chauhan](https://github.com/yash-vks-chauhan)

<!-- Add later when ready:
- Portfolio:
- LinkedIn:
- Resume:
- Email:
-->
