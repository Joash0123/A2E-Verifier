# A2E-Verifier

## AI Agent Authorization-to-Execution Verifier

A2E-Verifier is a security verification framework for AI-agent systems that checks whether an action that actually executes remains within the authorization originally granted to the agent.

It focuses on the security boundary between:

**Authorized Action → Transformed / Reconstructed Action → Actual Execution**

AI-agent workflows can modify actions between authorization and execution. A2E-Verifier detects when the executed action no longer preserves the original authorization.

---

## Live Demo

**Web Application:**
https://a2e-verifier.onrender.com/

**API Documentation:**
https://a2e-verifier.onrender.com/docs

---

## Why A2E-Verifier?

Traditional authorization checks commonly ask:

> Is this action authorized?

A2E-Verifier asks:

> Does the action that actually executes still preserve the authorization that was originally granted?

For example:

```text
Authorized:
database.read(customer/123)

Executed:
database.delete(customer/123)

Result:
BLOCK
OPERATION_DRIFT
```

Another example:

```text
Authorized:
database.read(customer/123)

Executed:
database.read(customer/456)

Result:
BLOCK
RESOURCE_DRIFT
```

---

## What It Detects

A2E-Verifier validates multiple dimensions of authorization integrity:

| Dimension  | Example                                    |
| ---------- | ------------------------------------------ |
| Tool       | Authorized tool differs from executed tool |
| Operation  | `read` → `delete`                          |
| Resource   | `customer/123` → `customer/456`            |
| Parameters | Authorized parameters are modified         |
| Context    | Execution context changes                  |
| Actor      | `support-agent` → `admin`                  |

Detected security categories include:

* `RESOURCE_DRIFT`
* `OPERATION_DRIFT`
* `PARAMETER_DRIFT`
* `ACTOR_DRIFT`
* Context drift
* Tool drift

The verifier produces:

* Allow / block decision
* Verdict
* Authorized action
* Executed action
* Investigation summary
* Drift category
* Evidence
* Remediation guidance

---

## Architecture

```text
                    AI Agent / Application
                             |
                             v
                    Authorized Action
                             |
                             v
                  Transformation / Routing
                             |
                             v
                     Executed Action
                             |
                             v
              +---------------------------+
              |       A2E-Verifier        |
              |---------------------------|
              | Tool                      |
              | Operation                 |
              | Resource                  |
              | Parameters                |
              | Context                   |
              | Actor                     |
              | Integrity / Provenance     |
              +-------------+-------------+
                            |
                   +--------+--------+
                   |                 |
                Allowed           Blocked
                   |                 |
                   v                 v
               Execution       Investigation
                                     |
                                     v
                            Evidence + Remediation
```

---

## How It Works

An action is represented using:

```python
Action(
    tool=...,
    operation=...,
    resource=...,
    parameters=...,
    context=...,
    actor=...,
)
```

The verifier compares the **authorized action** with the **executed action**.

If the relevant authorization properties remain unchanged:

```text
MATCH
allowed = True
```

If the executed action exceeds or changes the original authorization:

```text
MISMATCH
allowed = False
```

The investigation layer then identifies the type of drift and provides supporting evidence and remediation guidance.

---

## API

### `POST /verify`

Compares an authorized action with an executed action.

Example:

```json
{
  "authorized": {
    "tool": "database",
    "operation": "read",
    "resource": "customer/123",
    "parameters": {},
    "context": {},
    "actor": "support-agent"
  },
  "executed": {
    "tool": "database",
    "operation": "read",
    "resource": "customer/456",
    "parameters": {},
    "context": {},
    "actor": "support-agent"
  }
}
```

Result:

```text
allowed  : False
verdict  : RESOURCE_MISMATCH
category : RESOURCE_DRIFT
```

### `GET /scenarios`

Returns the built-in authorization-to-execution security scenarios.

### `GET /benchmark`

Runs the registered benchmark suite and returns detection and false-positive metrics.

### `GET /health`

Returns the service health status.

---

## Built-in Security Scenarios

The project includes representative authorization-to-execution mismatch scenarios:

1. Resource substitution
2. Operation escalation
3. Actor substitution
4. Parameter escalation

These scenarios are also exposed through the API.

---

## Investigation Layer

A2E-Verifier does more than return a simple allow/block decision.

```text
Decision
   ↓
Mismatch Category
   ↓
Evidence
   ↓
Security Explanation
   ↓
Remediation Guidance
```

This makes the system useful for security testing, debugging, auditing, and security demonstrations.

---

## Benchmark and Testing

The project contains a comprehensive automated test suite covering:

* Action models
* Verification logic
* API behavior
* Security scenarios
* Investigation
* Reporting
* Provenance
* Integrity
* Benchmark functionality

Current test status:

```text
869 passed
1 warning
```

The deployed API has also been manually validated against the live Render deployment for:

* Exact authorized execution
* Resource substitution
* Operation escalation
* Actor substitution
* Parameter escalation

---

## Technology Stack

* Python 3.10+
* FastAPI
* Pydantic
* Pytest
* Uvicorn
* HTML
* CSS
* JavaScript
* Render

The frontend is lightweight and does not require a large JavaScript framework.

---

## Project Structure

```text
A2E-Verifier/
│
├── a2e_verifier/
│   ├── action.py
│   ├── verifier.py
│   ├── investigation.py
│   ├── scenarios.py
│   ├── benchmark_registry.py
│   ├── registry_benchmark.py
│   ├── provenance.py
│   ├── integrity.py
│   └── ...
│
├── api/
│   └── main.py
│
├── tests/
│   └── ...
│
├── web/
│   ├── index.html
│   └── static/
│       ├── app.js
│       └── style.css
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/Joash0123/A2E-Verifier.git
cd A2E-Verifier
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest -q
```

Start the API:

```bash
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Open-Source Foundation

A2E-Verifier was developed by extending the open-source **AgentLock** project rather than building every component from scratch.

Original project:

https://github.com/webpro255/agentlock

The original project is licensed under the Apache License 2.0.

A2E-Verifier adds a dedicated authorization-to-execution verification layer, including:

* Action comparison
* Authorization drift detection
* Investigation
* Security scenarios
* Benchmarking
* Provenance and integrity functionality
* API exposure
* Dedicated web interface

The applicable license and attribution information are included in `LICENSE`.

---

## Security Scope

A2E-Verifier is intended for:

* AI-agent security research
* Authorization testing
* Application security testing
* Security validation
* Defensive security engineering
* Authorized penetration-testing environments
* Security education and demonstrations

Use the framework only against systems and environments for which you have authorization.

---

## Core Security Property

A2E-Verifier is built around one central security property:

```text
The action that executes should not exceed
the authority that was originally granted.
```

A2E-Verifier provides a practical mechanism for testing that property across the authorization-to-execution boundary.

---

## Author

**Joash Paspula**

GitHub:
https://github.com/Joash0123
