#!/usr/bin/env python3
"""
TextbeltRequest class
reads speedtest.log and creates an average for yesterday, texts it to your
phone and checks if sent
logs to sterr
"""
import re
from datetime import datetime
from datetime import timedelta
from time import sleep
import os

import requests

from speedtest_sendtest.logging import create_logger
from speedtest_sendtest.speedtest_exceptions import SpeedtestNoSpeedsError
from speedtest_sendtest.speedtest_exceptions import SpeedtestAttemptsExceededError


def main():
    "tester"
    requester = TextBeltRequest()
    if requester.success:
        print("Success")
    else:
        print("Failure")


class TextBeltRequest():
    """
    Class for TextBeltRequest
    :attributes
        attempts - cannot exceed 4 or errors
        logger - logger from create_logger
        success - if delivery succeeded
    """

    def __init__(self, logger=True):
        self.attempts = 0
        self.success = None
        self.request = None
        if logger:
            self.logger = create_logger()
        self.speedtest_log = os.path.expanduser("~/speedtest.log")
        self.start_request()

    def __str__(self):
        print(__name__ + ": " + self.success)

    def start_request(self):
        """Main try statement, calls make_request and logs exceptions then removes speedtest.log"""
        try:
            self.logger.info("calling make_request")
            self.make_request()
        except SpeedtestAttemptsExceededError:
            self.logger.exception("Attempts succeeded, try again later")
        except SpeedtestNoSpeedsError:
            self.logger.exception(
                "No speeds found in speedtest.log, run speedtest and try again"
            )
        except requests.HTTPError:
            self.logger.exception(
                "Unsuccessful HTTP status code, check your request args")
        except requests.Timeout:
            self.logger.exception("Requests timed out, is Textbelt up?")
        except requests.ConnectionError:
            self.logger.exception(
                "Connection problem, check your internet, is Textbelt up?")
        except ValueError:
            self.logger.exception("Bad value")
        except FileNotFoundError:
            self.logger.exception("Speedtest.log doesn't exist, run speedtest")
        try:
            os.remove(self.speedtest_log)
        except FileNotFoundError:
            self.logger.exception("Speedtest.log doesn't exist, run speedtest")

    def make_request(self):
        """make the request and check if http response code was good"""
        self.logger.info("Calling make_average")
        average_speed = self.make_average()
        yesterday = datetime.today() - timedelta(days=1)
        self.logger.info("Making request")
        self.request = requests.post("https://textbelt.com/text", {
            "phone":
            8324589082,
            "message":
            "Average speed for {time} was {amount} Mbits/s".format(
                time=datetime.strftime(yesterday, "%a %b %d %Y"),
                amount=average_speed),
            "key":
            "596c1c51c19d9511a3e7008452f9d055c7a294b61hiJCfbyBOv3nSgH2RMNfYBYA"
        })
        self.request.raise_for_status()
        self.logger.info("Calling do_checks")
        self.do_checks()

    def make_average(self):
        """create averages from speedtest.log"""
        download_regex = re.compile(r"Download:\s(\d{1,2}\.\d{1,2})\s")
        amounts = []
        self.logger.info("Opening speedtest.log")
        with open(self.speedtest_log, "r") as file:
            for line in file:
                search = download_regex.search(line.rstrip())
                if search:
                    amounts.append(float(search.group(1)))
        average_speed = sum(amounts) / len(amounts)
        self.logger.info("Returning average speed if there are any")
        if average_speed:
            return average_speed
        else:
            raise SpeedtestNoSpeedsError("No speeds in speedtest.log")

    def do_checks(self):
        """Do all the checks,  warn if no quota remaining, set self.success to True"""
        if self.request.json()["quotaRemaining"] <= 5:
            self.logger.warning(
                "Textbelt quota less than or equal to 5, should fill up again")
        self.logger.info("Calling requests_check()")
        requests_check_response = self.requests_check()
        self.logger.info("Calling check_success()")
        check_success_response = self.check_success()
        self.logger.info("Calling check_sent()")
        check_sent_response = self.check_sent()
        if requests_check_response and check_success_response and check_sent_response:
            self.logger.info("Sent and received")
            self.success = True

    def requests_check(self):
        """
        check the request status code and retry if it didn't work, only up to 5 times
        """
        if self.request.status_code != requests.codes.ok and self.attempts < 5:
            self.logger.error("Request didn't go through with status code: %s",
                              self.request.status_code)
            self.logger.debug("Incrementing attempts, attempts: %s",
                              self.attempts)
            self.attempts += 1
            self.logger.info("Recalling make_request()")
            self.make_request()
        elif self.attempts == 5:
            raise SpeedtestAttemptsExceededError("Attempts exceeded")
        elif self.request.status_code == requests.codes.ok:
            return True
        else:
            raise ValueError(
                "Unexpected combination of self.attempts and self.request.status code. With self.attempts: %s, and status_code: %s",
                self.attempts, self.request.status_code)

    def check_sent(self):
        """Query Textbelt if the message is delivered and retry if not"""
        loop = 0
        while loop < 5:
            self.logger.debug("loop: %s", loop)
            query = requests.get("https://textbelt.com/status/{}".format(
                self.request.json()["textId"]))
            self.request.raise_for_status()
            if query.json()["status"] == "DELIVERED":
                self.logger.info("Message Delivered")
                return True

            elif query.json()["status"] == "SENDING":
                self.logger.info("Message sending, checking back in 5 sec")
                sleep(5)
                loop += 1

            elif query.json()["status"] == "FAILED":
                self.logger.error("Message failed, retrying")
                self.attempts += 1
                self.make_request()

            elif query.json()["status"] == "UNKOWN":
                self.logger.warning(
                    "Don't know what happened to message, rechecking in 5 sec")
                self.logger.info("")
                loop += 1
                sleep(5)
            else:
                raise ValueError("query.json() returned an unexpected value")
        else:
            raise ValueError(
                "Either textbelt took longer than 25 seconds to send or textbelt doesn't know what happened"
            )

    def check_success(self):
        "Checks for success in sending request to TextBelt"
        if not self.request.json()["success"] and self.attempts < 5:
            self.logger.warning(
                "Textbelt message didn't send, error was: %s, trying again",
                self.request["error"])
            self.logger.debug("incrementing attempts")
            self.attempts += 1
            self.make_request()
        elif self.request.json()["success"]:
            return True
        elif self.attempts == 5:
            raise SpeedtestAttemptsExceededError("Attempts exceeded")
        else:
            raise ValueError(
                "Unexpected combination of self.request.json and self.attempts with self.request.json: %s and self.attempts: %s",
                self.request.json, self.attempts)


if __name__ == "__main__":
    main()
