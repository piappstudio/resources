import sys
import json
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_voting_results(url, button_text, participants=None):
    """
    Launches Chrome, clicks the result button, and captures voting data.
    Maps results to participants if provided.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    mapped_results = {}

    try:
        print(f"Navigating to {url}...")
        driver.get(url)
        time.sleep(5) # Allow JS to execute

        # 1. Scroll and Look for the Button (Handling Iframes)
        print("Scrolling to find result button...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)

        # Check in all iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframes. Searching for button...")

        found_button = False
        
        # Try main document first
        try:
            xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{button_text.lower()}')]"
            button = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)
            button.click()
            print(f"Clicked '{button_text}' in main document.")
            found_button = True
        except:
            pass

        if not found_button:
            for index, iframe in enumerate(iframes):
                try:
                    driver.switch_to.frame(iframe)
                    xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{button_text.lower()}')]"
                    button = driver.find_element(By.XPATH, xpath)
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(1)
                    button.click()
                    print(f"Clicked '{button_text}' in iframe {index}.")
                    found_button = True
                    break # Stop once found
                except:
                    driver.switch_to.default_content()

        if found_button:
            time.sleep(5) # Wait for results to render

        # 2. Extract Data (Check main and then iframes)
        def extract_names(d, p_list):
            results = {p: "Not found" for p in p_list}
            
            # Get all elements that contain a '%' character. 
            # We filter for those that have text but aren't just giant containers.
            all_elements = d.find_elements(By.XPATH, "//*[contains(., '%')]")
            
            # Sort by length of text (ascending) to check smaller, more specific elements first
            candidate_texts = []
            for el in all_elements:
                try:
                    t = el.text.strip().replace('\n', ' ')
                    if t and len(t) < 1000: # Ignore massive containers
                        candidate_texts.append(t.lower())
                except:
                    continue

            for p_name in p_list:
                p_lower = p_name.lower()
                # Advanced tokenization: split by spaces, dots, and camelCase
                import re
                clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', p_name)
                p_tokens = [t.lower() for t in clean_name.replace('.', ' ').split() if len(t) > 2]
                
                for text in candidate_texts:
                    # Match if full name is present
                    if p_lower in text:
                        results[p_name] = text
                        break
                    # Match if any significant token is present
                    if any(token in text for token in p_tokens):
                        results[p_name] = text
                        break
            return results

        if participants:
            print(f"Searching for {len(participants)} participants...")
            mapped_results = extract_names(driver, participants)
            
            # If not found in main, check iframes
            if all(v == "Not found" for v in mapped_results.values()):
                for index, iframe in enumerate(iframes):
                    try:
                        driver.switch_to.frame(iframe)
                        iframe_res = extract_names(driver, participants)
                        if any(v != "Not found" for v in iframe_res.values()):
                            mapped_results = iframe_res
                            print(f"Found participant data in iframe {index}.")
                            break
                    except:
                        pass
                    finally:
                        driver.switch_to.default_content()
        else:
            mapped_results["raw_generic"] = "No participants provided"

        return mapped_results

    except Exception as e:
        print(f"Error during scraping: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape BiggBoss voting results.')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('button_text', help='Text of the button to click for results')
    parser.add_argument('--participants', help='JSON string of participant names', default='[]')
    parser.add_argument('--main_json', help='Path to main.json to extract participant names')
    
    args = parser.parse_args()
    
    participant_list = []
    
    # Priority 1: Extract from main.json if path provided
    if args.main_json:
        try:
            with open(args.main_json, 'r') as f:
                main_data = json.load(f)
                participant_list = [p['name'] for p in main_data.get('participants', [])]
        except Exception as e:
            print(f"Error reading main.json: {e}")

    # Priority 2: Use explicitly passed participants (appended to list)
    if args.participants:
        try:
            passed_list = json.loads(args.participants)
            for name in passed_list:
                if name not in participant_list:
                    participant_list.append(name)
        except Exception as e:
            if not participant_list: # Only error if we have no names at all
                print(f"Error parsing participants JSON: {e}")
        
    data = get_voting_results(args.url, args.button_text, participant_list)
    if data:
        # Final output for the agent
        print("---RESULT_START---")
        print(json.dumps(data, indent=2))
        print("---RESULT_END---")
    else:
        sys.exit(1)
