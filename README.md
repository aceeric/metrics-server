# Python HTTP Server to experiment with Prometheus Query Language

The purpose of this Python project is to help learn the Prometheus Query Language (promql). When learning The query language, I found it helpful to be able to generate simple metrics in a controlled fashion. This enabled me to vary the metrics being fed to Prometheus, and observe the impact of those metrics on various promql expressions.
 
This project runs a simple Python HTTP Server that serves up three metrics in a controlled manner. The metrics are served on port 7890. I generally run this directly from PyCharm.
 
To use the tool, first run the app in PyCharm. Then, from the console, query the metrics using curl - this is exactly the same way that Prometheus would scrape the metrics. For example:
```shell script
watch curl -s http://localhost:7890/metrics
``` 

Which should produce output like:
```shell script
# HELP python_operations_counter Number of Operations Performed.
# TYPE python_operations_counter counter
python_operations_counter 362.0
# HELP python_operations_summary Total Operation Size.
# TYPE python_operations_summary summary
python_operations_summary_sum 1866.3
python_operations_summary_count 362.0
# HELP python_operations_gauge Operations Gauge.
# TYPE python_operations_gauge gauge
python_operations_gauge 9.0
```
The values should vary on each curl invocation. Once you've verified that the metrics are being exposed by the Python HTTP Server, then you can start Prometheus, and observe the metrics there. I've provided two artifacts in the `prometheus` directory to simplify that task:

The first artifact is a `prometheus.yml` file that defines the scrape configs for Prometheus to scrape this Python server on localhost.

The second is a simple shell script to start a docker container that pulls the provided configuration file into the container so that Prometheus will immediately start scraping. You run it thus:
```shell script
prometheus/start-prometheus-container
```
Assuming all is well (i.e. you have Docker running, etc.), you should see something like the following:
```shell script
WARNING: Published ports are discarded when using host network mode
72d026a3edb91f470648f35a377ef94e0fadeb4eee0793a5f3e87aad5a363b6b
```
And then if you execute the command `docker ps` you should see the running container:
```shell script
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
72d026a3edb9        prom/prometheus     "/bin/prometheus --c…"   11 seconds ago      Up 10 seconds                           prometheus
```
By default, Promethus is available on port 9090. So now, you can open up your your browser, and enter the URL `http://localhost:9090/graph`. Note - for me - my Firefox configuration by default blocks trackers, etc. So I need to click on the Firefox content blocking shield icon in next to the URL to turn off enhanced tracking protection. Otherwise the Promethus Web UI won't work.

Now that's done, you can start to query the metrics in Prometheus, and build expressions to understand how those expressions modify the presentation of the metrics being scraped from the Python server by Prometheus. And, you can modify the behavior of the metric generation in the Python HTTP Server, add new metrics, etc.

For example, clicking the `Console` tab in Prometheus, and querying the `python_operations_summary_sum` metric, produces one value on each execution. Entering `python_operations_summary_sum[2m]` returns all the values scraped by Prometheus over the last two minutes.

Once you're finished, you simply stop the HTTP Server in PyCharm, and stop the running docker container:
```shell script
docker container stop prometheus
```

There are many sources available that provide instruction regarding the Prometheus Query Language. It is not the intent of this project to duplicate that. This project simply provides a simple and accessible test bed to experiment with various metrics using the query language.