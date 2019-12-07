import time
# noinspection PyCompatibility
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock, Thread
from random import random

PORT = 7890
counter = 0
summary = 0
gauge = 0
counter_thread_running = True


class MyHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler. Ignores the actual request and only responds with
    the test metric in the form Prometheus expects it. E.g:

    # HELP python_operations_counter Number of Operations Performed.
    # TYPE python_operations_counter counter
    python_operations_counter 999.0
    """
    # noinspection PyPep8Naming
    def do_GET(self):
        global counter, summary, gauge, lock
        lock.acquire()
        my_counter = counter
        my_summary = summary
        my_gauge = gauge
        lock.release()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message =\
            "# HELP python_operations_counter Number of Operations Performed.\n"\
            "# TYPE python_operations_counter counter\n"\
            "python_operations_counter %.1f\n"\
            "# HELP python_operations_summary Total Operation Size.\n" \
            "# TYPE python_operations_summary summary\n" \
            "python_operations_summary_sum %.1f\n"\
            "python_operations_summary_count %.1f\n"\
            "# HELP python_operations_gauge Operations Gauge.\n" \
            "# TYPE python_operations_gauge gauge\n" \
            "python_operations_gauge %.1f\n" % (my_counter, my_summary, my_counter, my_gauge)
        self.wfile.write(bytes(message, "utf8"))


def generate_metric():
    """
    Function to run in a thread and increment a counter that is exposed as
    a metric by the 'MyHandler' class
    """
    global counter, summary, gauge, lock, counter_thread_running

    print("Metric thread started")
    while counter_thread_running:
        lock.acquire()
        """ Counters always go up """
        counter += 1
        """ Summaries always go up """
        summary += random() * 10
        """ Gauges can go up and down """
        gauge = random() * .5 * 20
        lock.release()
        time.sleep(random() / 3.0)
    print("Metric thread stopped")


# Create a lock to synchronize access to the counter for the generate_metric function, which
# runs in a thread, and the HTTP response handler
lock = Lock()

# Start up a thread to increment the metric counter
Thread(target=generate_metric).start()

# Create the HTTP server
httpd = HTTPServer(("127.0.0.1", PORT), MyHandler)

try:
    # Start the HTTP server. Control will return when the server is stopped, e.g.
    # by the user pressing CTRL-C
    print("Running server...")
    httpd.serve_forever()
except:
    print("Server stopped")
    httpd.server_close()
finally:
    # stop the metric counter thread
    counter_thread_running = False
