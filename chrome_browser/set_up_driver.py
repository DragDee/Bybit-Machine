import zipfile
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import os
import time
import undetected_chromedriver as uc
from selenium_stealth import stealth
from sqlalchemy.sql.functions import random

from models.proxy import Proxy
import random


class DriverSetUp:


    def get_chromedriver(self, proxy: Proxy = False, user_agent=None, option=None, headless=False):

        PROXY_HOST = ''
        PROXY_PORT = ''
        PROXY_USER = ''
        PROXY_PASS = ''

        if proxy:

            PROXY_HOST = proxy.ip
            PROXY_PORT = proxy.port  # Your proxy port
            PROXY_USER = proxy.proxy_login
            PROXY_PASS = proxy.proxy_password

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"76.0.0"
        }
        """

        background_js = """
        let config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


        chrome_options = uc.ChromeOptions()
        #chrome_options = webdriver.ChromeOptions()


        if proxy:
            from data.config import ROOT_DIR
            plugin_file = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr('manifest.json', manifest_json)
                zp.writestr('background.js', background_js)
                zp.extractall('unpacked_files')


            unpacked_files = os.path.join(ROOT_DIR, 'chrome_browser\\unpacked_files')
            chrome_options.add_argument(r'--load-extension=' + str(unpacked_files))


        if user_agent:
            chrome_options.add_argument(f'--user-agent={user_agent}')

        if option:
            chrome_options.add_argument(option)


        if headless:
            chrome_options.add_argument('--window-size=1920,1080')
            #chrome_options.add_argument("--headless=new")

            #chrome_options.add_argument("--window-position=-10000,-10000")
        chrome_options.add_argument('--window-size=1920,1080')


        chrome_options.add_argument("--disable-blink-features=AutomationControlled")


        driver = uc.Chrome(
            options=chrome_options

        )
        #driver = webdriver.Chrome(options=chrome_options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                  '''
        })

        r0 = random.randrange(6, 9)
        r1 = random.randrange(1000, 1999)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Google Inc. (NVIDIA)",
                renderer=f"ANGLE (NVIDIA, NVIDIA GeForce RTX 40{r0}0 (0x0000{r1}) Direct3D11 vs_5_0 ps_5_0, D3D11)",
                fix_hairline=True,
                )


        return driver



