# Pulse Check API (Watchdog Sentinel)

## Overview

Pulse Check API is a backend monitoring system designed to track remote devices using a heartbeat mechanism. Each device sends periodic signals to indicate it is alive. If a device fails to send a heartbeat within its configured timeout period, the system automatically marks it as down and triggers an alert.

This project demonstrates backend engineering skills including REST API design, state management, concurrency, and system monitoring.

---

## Problem Statement

CritMon Servers Inc. manages remote solar farms and weather stations in remote areas with unstable connectivity.

Devices are expected to send periodic "I'm alive" signals. However, there is currently no system to detect failures in real time when a device stops responding.

This system solves that by continuously monitoring device activity and triggering alerts when a device becomes inactive.

---

## Features

- Register monitoring devices with custom timeout values
- Receive heartbeat signals to reset device timers
- Automatic detection of inactive devices
- Background monitoring system using threading
- Device status tracking (active / down)
- Console-based alert system
- Retrieve all registered monitors

---

## Architecture Diagram

```mermaid id="diagram_fix"
sequenceDiagram
    participant Device
    participant API
    participant MemoryStore
    participant MonitorThread

    Device->>API: POST /monitors (register device)
    API->>MemoryStore: Save device with timeout

    loop Heartbeat cycle
        Device->>API: POST /monitors/{id}/heartbeat
        API->>MemoryStore: Update last_ping timestamp
    end

    loop Background check (every 5 seconds)
        MonitorThread->>MemoryStore: Check last_ping vs timeout

        alt Device timeout exceeded
            MonitorThread->>MemoryStore: Mark device as DOWN
            MonitorThread->>Console: Log ALERT message
        end
    end


API Endpoints
Register Monitor

POST /monitors

Request:

{
  "id": "device-123",
  "timeout": 60
}

Response:

{
  "message": "Monitor device-123 registered",
  "data": {
    "timeout": 60,
    "last_ping": 1710000000,
    "status": "active"
  }
}
Get All Monitors

GET /monitors

Response:

{
  "device-123": {
    "timeout": 60,
    "last_ping": 1710000000,
    "status": "active"
  }
}
Heartbeat

POST /monitors/{device_id}/heartbeat

Response:

{
  "message": "Heartbeat received from device-123",
  "data": {
    "timeout": 60,
    "last_ping": 1710000000,
    "status": "active"
  }
}
Alert System

When a device fails to send a heartbeat within its timeout period, the system triggers an alert:

{
  "ALERT": "Device device-123 is down!",
  "time": 1710000000
}

This is printed in the console to simulate real-world alerting.

How It Works
Device registers with ID and timeout
Server stores device state in memory
Device sends periodic heartbeat requests
Background thread continuously checks timestamps
If timeout is exceeded, device is marked as down
Alert is triggered in console
Setup Instructions

Install dependencies:

pip install flask

Run the application:

python app.py
Project Structure
pulse-check-api/
├── app.py
├── README.md
└── .gitignore
Developer Improvement
Input Validation Feature

Added validation to ensure:

Required fields exist (id, timeout)
Invalid requests are rejected safely
Why this matters

This prevents:

System crashes from bad input
Inconsistent data states
Unsafe API usage

It improves reliability and production readiness.

Technologies Used
Python
Flask
Threading
Time module
