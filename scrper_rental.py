from playwright.sync_api import sync_playwright
import time
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def dump_data(data, file_number):
    # Dump to JSON file
    json_filename = f'extracted_data_{file_number}.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f"Data dumped to {json_filename}")

def run(playwright):
    try:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        logging.info("Navigating to the website")
        page.goto("https://hip.huurcommissie.nl/p/uitspraken")

        logging.info("Waiting for and clicking the 'zoek' button")
        zoek_button = page.wait_for_selector('button:has-text("zoek")', state='visible', timeout=30000)
        if zoek_button:
            zoek_button.click()
        else:
            logging.error("'zoek' button not found")
            return

        logging.info("Waiting for initial results to load")
        page.wait_for_load_state('networkidle')

        all_li_texts = []
        file_number = 1

        while True:
            logging.info("Extracting text from <li> elements")
            li_elements = page.query_selector_all('li')
            for li in li_elements:
                page.click('text="Meer informatie"')

                text_content = li.inner_text()
                if text_content and text_content not in all_li_texts:
                    all_li_texts.append(text_content)

                    if len(all_li_texts) % 100 == 0:
                        data_to_dump = {str(i): text for i, text in enumerate(all_li_texts[-100:], len(all_li_texts) - 99)}
                        dump_data(data_to_dump, file_number)
                        file_number += 1

            logging.info(f"Total items extracted so far: {len(all_li_texts)}")

            load_more_button = page.query_selector('.btn.mx-button.mx-listview-loadMore')
            if load_more_button and load_more_button.is_visible():
                logging.info("Clicking 'load more' button")
                load_more_button.click()
                page.wait_for_load_state('networkidle')
                time.sleep(2)
            else:
                logging.info("No more 'load more' button found or it's not visible. Extraction complete.")
                break


        if len(all_li_texts) % 100 != 0:
            remaining_count = len(all_li_texts) % 100
            data_to_dump = {str(i): text for i, text in enumerate(all_li_texts[-remaining_count:], len(all_li_texts) - remaining_count + 1)}
            dump_data(data_to_dump, file_number)

        logging.info(f"Total items extracted: {len(all_li_texts)}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    finally:
        if 'browser' in locals():
            browser.close()

with sync_playwright() as playwright:
    run(playwright)
