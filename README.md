PulseCheck
==========

> Unified health, liveness, and readiness checks for Python microservices.

PulseCheck is a framework-agnostic health check library designed for modern Python services.

It provides a pluggable health engine with adapters for FastAPI and Django, built around Kubernetes liveness and readiness semantics.

* * * * *

Features
----------

-   Framework-agnostic core

-   FastAPI adapter

-   Django adapter

-   Pluggable dependency checks:

    -   SQLAlchemy (async & sync)

    -   Django ORM

    -   Redis (async & sync)

    -   RabbitMQ (Kombu)

    -   Celery worker inspection

    -   HTTP dependency checks

-   Configurable timeouts

-   Degraded vs unhealthy states

-   Optional dependency extras

-   Zero forced framework pollution

-   Production-ready JSON schema

-   Kubernetes-compatible design

* * * * *

Installation
------------

### Core only
```python
pip install pulsecheck-py
```
### With FastAPI support
```python 
pip install pulsecheck-py[fastapi]
```
### With Django support
```python
pip install pulsecheck-py[django]
```
### With selected dependency checks
```python
pip install pulsecheck-py[fastapi,redis_async,sqlalchemy_async,rabbitmq,celery]
```
Only install what you use.\
PulseCheck does **not** force optional frameworks or libraries.

* * * * *

FastAPI Example
===============
```python
from fastapi import FastAPI
from pulsecheck.core import HealthRegistry
from pulsecheck.core.checks import SQLAlchemyAsyncCheck
from pulsecheck.fastapi import make_health_router

from app.database import engine

app = FastAPI()

registry = HealthRegistry(environment="prod")
registry.register(SQLAlchemyAsyncCheck(engine))

app.include_router(make_health_router(registry))

### Sync SQLAlchemy example

from pulsecheck.core.checks import SQLAlchemySyncCheck

registry.register(SQLAlchemySyncCheck(engine))
```
* * * * *

Endpoints
---------
```text
GET /health
GET /health/live
GET /health/ready
```
These follow Kubernetes semantics:

-   `/live`, container is alive

-   `/ready`,  dependencies are available

-   `/health`, full aggregated state

* * * * *

Django Example
==============
```python
from pulsecheck.core import HealthRegistry
from pulsecheck.core.checks import DjangoDBCheck
from pulsecheck.django import make_urlpatterns

registry = HealthRegistry(environment="prod")
registry.register(DjangoDBCheck())

urlpatterns = [
    *make_urlpatterns(registry)
]
```
* * * * *

Health Response Format
======================
```json
{
  "status": "HEALTHY",
  "timestamp": "2026-02-15T12:34:56Z",
  "environment": "prod",
  "checks": {
    "database": {
      "status": "HEALTHY",
      "response_time_ms": 4.3
    }
  }
}
```
* * * * *

Health States
-------------

-   `HEALTHY`, dependency available

-   `DEGRADED`, dependency responding but slow

-   `UNHEALTHY`, dependency unavailable or failing

* * * * *

Optional Dependencies (Extras)
==============================

PulseCheck uses optional extras to avoid unnecessary framework coupling.

| Extra | Installs |
| --- | --- |
| fastapi | FastAPI adapter |
| django | Django adapter |
| redis_async | Async Redis check |
| redis_sync | Sync Redis check |
| rabbitmq | Kombu-based AMQP check |
| celery | Celery inspect check |
| sqlalchemy_async | Async SQLAlchemy check |
| http | HTTP dependency check |

If a dependency is not installed and you try to use its check, a clear runtime error is raised.

* * * * *

Design Philosophy
=================

PulseCheck separates:

-   Core health aggregation logic

-   Dependency checks

-   Framework adapters

This ensures:

-   No tight framework coupling

-   Optional ecosystem integration

-   Clean dependency graphs

-   Microservice-friendly architecture

-   No forced imports of unused frameworks

Optional checks are lazily loaded - installing `pulsecheck-py` alone does not pull Django, FastAPI, Celery, Redis, etc.

* * * * *

Kubernetes Usage Pattern
========================

Recommended deployment model:

-   API container,  checks DB, Redis, required dependencies

-   Worker container, checks broker connectivity

-   Do not couple unrelated services in readiness checks

Health checks should represent **required runtime dependencies**, not the entire distributed system.

* * * * *

Intended Use
============

PulseCheck is designed for:

-   Microservices

-   Containerized applications

-   Kubernetes environments

-   Internal APIs

-   Distributed systems

It is **not** a monitoring system.

It is a lightweight dependency availability indicator.

* * * * *

Testing
=======

PulseCheck is tested against:

-   Python 3.10+

-   FastAPI

-   Django

-   Async and sync dependency scenarios

* * * * *

Contributing
============

Issues and pull requests are welcome.