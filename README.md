# Yash Chauhan

<p>
  <a href="https://www.linkedin.com/in/yash-vks-chauhan"><img src="https://img.shields.io/badge/LinkedIn-yash--vks--chauhan-0D1117?style=flat-square&logo=linkedin&logoColor=white&labelColor=0D1117&color=2563EB" alt="LinkedIn"></a>
  <a href="https://github.com/yash-vks-chauhan?tab=repositories"><img src="https://img.shields.io/badge/GitHub-projects-0D1117?style=flat-square&logo=github&logoColor=white&labelColor=0D1117&color=64748B" alt="GitHub projects"></a>
  <img src="https://img.shields.io/badge/CSE_AI%2FML-SRM-0D1117?style=flat-square&labelColor=0D1117&color=14B8A6" alt="CSE AI/ML at SRM">
  <img src="https://img.shields.io/badge/AWS-ML_Specialty-0D1117?style=flat-square&logo=amazonwebservices&logoColor=white&labelColor=0D1117&color=F59E0B" alt="AWS ML Specialty">
</p>

```txt
run ./yash

> builds:      AI systems, ML pipelines, full-stack products
> likes:       metrics, traces, recovery paths, dashboards
> recent:      IIT Madras research + Hindalco predictive maintenance
> current:     turning model demos into inspectable systems
```

I am a CSE student specializing in AI/ML. I like building things where the interesting part is not hidden behind a single model call: the data pipeline, the failure path, the dashboard, the metric, the fallback, and the reason a decision was made.

## Open A Drawer

<details open>
<summary><kbd>01</kbd> <strong>Fast scan</strong></summary>

| Signal | Snapshot |
| --- | --- |
| Education | B.Tech CSE, Artificial Intelligence & Machine Learning, SRM Institute of Science and Technology |
| Research | IIT Madras research intern working with emergency medical response data |
| Industry | Hindalco predictive-maintenance intern using historian data and anomaly detection |
| Main lanes | AI systems, observability, applied ML, full-stack product engineering |
| Certifications | AWS Cloud Practitioner, AWS Certified Machine Learning - Specialty, DeepLearning.AI ML/DL specializations |

</details>

<details>
<summary><kbd>02</kbd> <strong>Research drawer</strong> - ambulance response analytics</summary>

Worked on emergency medical response analytics at IIT Madras using Tamil Nadu 108 EMS registry data.

| Built / Analyzed | Detail |
| --- | --- |
| Dataset scale | 3.59M ambulance dispatch records from 2017-2025 |
| Coverage | 38 districts and 44 emergency types |
| Detection | Autoencoder pipeline identifying 8,567 anomalous dispatch events |
| Benchmarking | XGBoost counterfactual model with WMAPE 8.37% |
| Metrics | Time Drift Index and Quantum Stability Index for operational stability |
| Simulation | 5,000+ ambulance trips with peak-hour, monsoon, and construction-delay scenarios |

`Python` `Pandas` `NumPy` `SciPy` `XGBoost` `SHAP` `OSMnx` `NetworkX` `Folium`

</details>

<details>
<summary><kbd>03</kbd> <strong>Systems drawer</strong> - incidents, Kubernetes, self-healing</summary>

[AutoScaler](https://github.com/yash-vks-chauhan/Autoscaler) is my systems-heavy project: a Kubernetes observability and self-healing platform.

- 3-node Kind cluster from day one, not a Docker Compose mock.
- Isolation Forest for multivariate spikes, LSTM autoencoder for slow degradation, LLM reasoning for root-cause analysis.
- Random Forest fallback runs in-cluster when external model providers are unavailable.
- SHAP explanations surface per-metric feature importance.
- Chaos Engine injects 6 failure types across 3 intensity levels.
- Watchdog health-checks 7 components every 30 seconds.

`Kubernetes` `Docker` `Prometheus` `TimescaleDB` `Redis` `NestJS` `FastAPI` `Next.js` `SHAP`

</details>

<details>
<summary><kbd>04</kbd> <strong>ML drawer</strong> - images, sensors, model quality</summary>

[CT-Denoising-U-Net](https://github.com/yash-vks-chauhan/CT-Denoising-U-Net) is a medical-imaging pipeline for denoising CT and X-ray scans.

- Mixed-precision U-Net for medical image artifact reduction.
- About 12 dB PSNR gain and about 95% noise reduction on lung CT slices.
- Per-image PSNR / SSIM / MSE tracking across validation scans.
- Streamlit dashboard for noisy | clean | denoised comparisons.

At Hindalco, I worked on predictive maintenance using Proficy Historian, MTell, ARIMA, anomaly detection, and Power BI. Resume impact: 20% lower unscheduled downtime and 15% lower maintenance cost.

`TensorFlow` `Keras` `OpenCV` `scikit-image` `ARIMA` `Power BI` `Jupyter`

</details>

<details>
<summary><kbd>05</kbd> <strong>Product drawer</strong> - full-stack apps with real workflows</summary>

[KalaKraft](https://github.com/yash-vks-chauhan/Kalakraftdev) is a full-stack marketplace for hand-crafted resin art.

- Storefront for browsing, buying, and tracking artisan products.
- Admin dashboard for inventory, coupons, reviews, users, support tickets, and revenue metrics.
- Image/video pipeline with Sharp + Cloudinary.
- Firebase / NextAuth authentication and role-based access.
- Real-time order updates and low-stock alerts with Pusher.
- Email flows through Sendinblue and Vercel preview deployments.

`Next.js` `React` `TypeScript` `PostgreSQL` `Prisma` `Firebase` `Cloudinary` `Pusher` `Vercel`

</details>

## Case Files

| Case | Open it | What to look for |
| --- | --- | --- |
| `case-001` | [GlassBox](https://github.com/yash-vks-chauhan/Glassbox) | Grounded AI, refusal routing, audit replay, trust scoring |
| `case-002` | [AutoScaler](https://github.com/yash-vks-chauhan/Autoscaler) | Kubernetes, anomaly detection, chaos testing, explainability |
| `case-003` | [CT-Denoising-U-Net](https://github.com/yash-vks-chauhan/CT-Denoising-U-Net) | U-Net training, medical image quality metrics, Streamlit inspection |
| `case-004` | [KalaKraft](https://github.com/yash-vks-chauhan/Kalakraftdev) | Product flows, admin workflows, auth, real-time features |

## Scoreboard

| 3.59M | 8,567 | 8.37% | ~12 dB | 20% |
| --- | --- | --- | --- | --- |
| EMS records analyzed | anomalous dispatch events | XGBoost WMAPE | PSNR gain | downtime reduction |

## Toolbox

<p>
  <img src="https://img.shields.io/badge/Python-111827?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TypeScript-111827?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/FastAPI-111827?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-111827?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/TensorFlow-111827?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/scikit--learn-111827?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/PostgreSQL-111827?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-111827?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Kubernetes-111827?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/Prometheus-111827?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus">
</p>

## Engineering Taste

I like projects where the hard parts are inspectable: what data entered, what changed, what confidence means, what failed, what recovered, and what evidence is left behind.

<!-- Add when ready:
- Portfolio:
- Resume:
- Email:
-->
