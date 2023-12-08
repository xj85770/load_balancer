# Load Balancer Project

## Introduction

**This Load Balancer project** is a simple yet functional implementation of a load balancing system. It distributes incoming HTTP requests across multiple backend servers using a round-robin scheduling algorithm and maintains high availability by performing regular health checks on the servers. The project is intended for educational purposes and provides a foundational understanding of how load balancers work in a networked environment.

## Requirements

- **Python 3.x**
- Basic understanding of networking and HTTP protocol
- Backend servers running on different ports for load balancing (e.g., Python's built-in HTTP server)

## Installation

No additional installation is required, as the script uses Python's built-in libraries. Ensure that Python 3.x is installed on your system.

## Running the Load Balancer

### Start Backend Servers:

Ensure that you have at least two backend servers running on different ports.

Example command to start a simple HTTP server in Python:
```bash
python -m http.server 8080 --directory server8080
```
Repeat the command for different ports and directories as needed.

### Run the Load Balancer:

1. Clone or download the load balancer script from the repository.
2. Run the script using Python:
   ```bash
   python load_balancer.py
   ```
   The load balancer will start on port 80 by default.

## Usage

After starting the load balancer, send HTTP requests to `http://localhost/`. The load balancer will forward the requests to the backend servers in a round-robin fashion. The health check mechanism will periodically check the availability of the backend servers. Unhealthy servers will be temporarily removed from the round-robin pool until they pass the health check again.

---

The health check mechanism will periodically check the availability of the backend servers.
Unhealthy servers will be temporarily removed from the round-robin pool until they pass the health check again.
