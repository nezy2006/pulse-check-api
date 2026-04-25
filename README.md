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



