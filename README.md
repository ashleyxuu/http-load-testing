# HTTP Load-Testing Tool

This tool allows you to perform load testing on HTTP endpoints. You can specify the queries per second (QPS) and the duration for the test, and it reports latencies and error rates.

## Features

- Generates HTTP requests at a specified QPS.
- Measures response latencies and reports errors.
- Asynchronous design for handling multiple requests concurrently.
- Dockerized for easy setup and usage.

## Requirements

- [Docker](https://www.docker.com/) installed on your system.

## Getting Started

### 1. Clone the Repository

Clone the repository to your local machine.

```bash
git clone https://github.com/yourusername/http-load-testing.git
cd http-load-testing
```

### 2. Build the Docker Image
Use the Dockerfile to build the Docker image.

```bash
docker build -t http-load-tester .
```

### 3. Run the Docker Container
Run the container, specifying the URL, QPS, and duration. Replace `http://example.com` with your target URL.

```bash
docker run --rm http-load-tester http://example.com --qps 5 --duration 30
```
Command-Line Arguments
- ``URL``: The URL to test.
- ``--qps``: Queries per second (default: 1).
- ``--duration``: Duration of the test in seconds (default: 10).

### 4. Example Usage
Test Google's Homepage at 5 QPS for 30 Seconds
```bash
docker run --rm http-load-tester http://www.google.com --qps 5 --duration 30
```

Output
The output will include average latency, latency standard deviation, total requests, and errors.

```
Average Latency: 0.23s
Latency Standard Deviation: 0.05s
Total Requests: 150
Errors: 0
```


## Development and Debugging
Access the Docker Container
You can run a bash shell inside the container for debugging:

```bash
docker run -it --entrypoint /bin/bash http-load-tester
```
Manual Run Inside Container
After accessing the container, you can run the script manually for testing:

```bash
python load_tester.py http://www.example.com --qps 5 --duration 30
```

## Files
- ``load_tester.py``: The main Python script for load testing.
- ``Dockerfile``: Dockerfile to build the Docker image.
- ``README.md``: This README file.


## Notes
- Ensure your target URL is accessible and returns a valid response.
- The tool uses ``aiohttp`` for asynchronous HTTP requests.
- This tool is for testing and educational purposes only. Use responsibly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
