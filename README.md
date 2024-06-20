# HTTP Load-Testing Tool

This tool allows you to perform load testing on HTTP endpoints. You can specify the queries per second (QPS) and the duration for the test, and it reports latencies and error rates.

## Features

- Generates HTTP requests at a specified QPS.
- Measures response latencies and reports error rate.
- Asynchronous design for handling multiple requests concurrently.
- Dockerized for easy setup and usage.

## Requirements

- [Docker](https://www.docker.com/) installed on your system.

## Getting Started

### 1. Clone the Repository

Clone the repository to your local machine.

```bash
git clone git@github.com:ashleyxuu/http-load-testing.git
cd http-load-testing
```

### 2. Build the Docker Image
Use the Dockerfile to build the Docker image.

```bash
docker build -t http-load-tester .
```

### 3. Run the Docker Container
Run the container, specifying the URL, QPS, and duration. Replace `http://example.com` with your target URL.

Run in default:
```bash
docker run --rm http-load-tester http://example.com
```

You can specify the QPS and duration.

```bash
docker run --rm http-load-tester http://example.com --qps 5 --duration 30
```
Command-Line Arguments:
- ``URL``: The URL to test.
- ``--qps``: Queries per second (default: 1).
- ``--duration``: Duration of the test in seconds (default: 10).

### 4. Example Usage
Test [Fireworks AI's Homepage](https://fireworks.ai) at 2 QPS for 5 Seconds.
```bash
docker run --rm http-load-tester https://fireworks.ai --qps 2 --duration 5
```

**Output**

The output will include average latency, latency standard deviation, total requests, and errors.

```
Progress: 100%|██████████| 10/10 [00:05<00:00,  1.99req/s]

Average Latency: 0.12s
Latency Standard Deviation: 0.03s
Total Requests: 10
Error rate: 0.00%
```


## Development and Debugging
Access the Docker Container:

You can run a bash shell inside the container for debugging:

```bash
docker run -it --entrypoint /bin/bash http-load-tester
```
Manual Run Inside Container:

After accessing the container, you can run the script manually for testing:

```bash
docker run --rm http-load-tester https://fireworks.ai --qps 2 --duration 5
```

## Files
- ``load_tester.py``: The main Python script for load testing.
- ``Dockerfile``: Dockerfile to build the Docker image.
- ``README.md``: This README file.


## Notes
- Ensure your target URL is accessible and returns a valid response.
- The tool uses ``aiohttp`` for asynchronous HTTP requests.
- This tool is for testing and educational purposes only. Use responsibly.
- You should give valid positive numbers for qps and duration.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
