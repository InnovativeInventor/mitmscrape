import glob
import json
import subprocess
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Scraper:
    def __init__(
        self,
        executable_path: str = "./chromedriver",
        url: str = "https://example.com",
        headless: bool = False,
        recursion: int = 1,
        path: str = ""
    ):
        self.proxy = self.start_proxy()
        self.url = url
        self.visited_urls = []

        if not path:
            self.path = "/".join(self.url.split("/")[:-1])

        try:
            chrome_options = Options()
            chrome_options.add_argument("ignore-certificate-errors")

            if headless:
                chrome_options.add_argument("--headless")

            capabilities = self.configure_proxy()

            self.driver = webdriver.Chrome(
                executable_path=executable_path,
                options=chrome_options,
                desired_capabilities=capabilities,
            )
            self.driver.implicitly_wait(3)

            self.page = self.get(self.url)

            self.scrape(recursion=recursion)

        finally:
            self.end_proxy()

    def start_proxy(self):
        return subprocess.Popen(
            ["mitmdump", "-w", "results"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

    def end_proxy(self):
        self.proxy.terminate()
        time.sleep(1)
        self.proxy.kill()

    def get(self, url: str):
        if not url in self.visited_urls:
            self.driver.get(url)
            self.visited_urls.append(url)

    def scrape(self, recursion=1, depth=0):
        if depth < recursion:
            remaining_links = set()
            links = self.driver.find_elements_by_tag_name("a")

            print(len(links))

            for each_link in links:
                remaining_links.add(each_link.get_attribute("href"))

            for each_link in remaining_links:
                if each_link and each_link.startswith(self.path):
                    self.get(each_link)
                    self.scrape(recursion=recursion, depth=depth + 1)

    def configure_proxy(self):
        # Credit: https://stackoverflow.com/questions/17082425/running-selenium-webdriver-with-a-proxy-in-python
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL

        # Proxy IP & Port
        prox.http_proxy = "0.0.0.0:8080"
        prox.ssl_proxy = "0.0.0.0:8080"

        # Configure capabilities
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)

        return capabilities


if __name__ == "__main__":
    fetcher = Scraper(url=sys.argv[1], recursion=int(sys.argv[2]))
