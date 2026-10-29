"""
MUJ SLCM Feedback Helper

Fills unanswered YES/NO radio groups with YES and selects Yes in visible
dropdowns that are still at their placeholder value. It does not submit forms.
"""

from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)

SLCM_URL = "https://mujslcm.jaipur.manipal.edu/"


def label_text(radio):
    """Return the text in the radio input's enclosing label, if present."""
    try:
        label = radio.find_element(By.XPATH, "./ancestor::label[1]")
        return label.text.strip().upper()
    except NoSuchElementException:
        return ""


def fill_unanswered_radio_groups(driver):
    groups = defaultdict(list)

    for radio in driver.find_elements(
        By.CSS_SELECTOR, 'input[type="radio"][name]'
    ):
        name = radio.get_attribute("name")
        if name:
            groups[name].append(radio)

    print(f"\nRadio groups found: {len(groups)}")
    changed = 0
    skipped = 0

    for name, radios in groups.items():
        try:
            if any(radio.is_selected() for radio in radios):
                skipped += 1
                continue

            yes_radio = next(
                (radio for radio in radios if label_text(radio) == "YES"),
                None,
            )

            if yes_radio is None:
                print(f"  [SKIP] No YES option found for group: {name}")
                skipped += 1
                continue

            label = yes_radio.find_element(
                By.XPATH, "./ancestor::label[1]"
            )
            if not label.is_displayed():
                print(f"  [SKIP] YES label is not visible: {name}")
                skipped += 1
                continue

            label.click()
            print(f"  [YES] Radio group: {name}")
            changed += 1

        except (
            ElementNotInteractableException,
            StaleElementReferenceException,
            NoSuchElementException,
        ) as exc:
            print(f"  [SKIP] Could not update radio group {name}: {exc.__class__.__name__}")
            skipped += 1

    return changed, skipped


def fill_placeholder_dropdowns(driver):
    changed = 0
    skipped = 0
    dropdowns = driver.find_elements(By.TAG_NAME, "select")

    print(f"\nDropdowns found: {len(dropdowns)}")

    for index, element in enumerate(dropdowns, start=1):
        try:
            if not element.is_displayed() or not element.is_enabled():
                continue

            select = Select(element)
            current = select.first_selected_option.text.strip().upper()

            options_by_text = {
                option.text.strip().upper(): option.text.strip()
                for option in select.options
            }

            if "YES" not in options_by_text:
                continue

            if current == "YES":
                continue

            # Do not overwrite a real existing answer such as No.
            if current not in ("SELECT", ""):
                print(f"  [KEEP] Dropdown {index} already has '{current}'")
                skipped += 1
                continue

            select.select_by_visible_text(options_by_text["YES"])
            print(f"  [YES] Dropdown {index}")
            changed += 1

        except (
            ElementNotInteractableException,
            StaleElementReferenceException,
            NoSuchElementException,
        ) as exc:
            print(f"  [SKIP] Could not update dropdown {index}: {exc.__class__.__name__}")
            skipped += 1

    return changed, skipped


def fill_current_questionnaire(driver):
    radio_changed, radio_skipped = fill_unanswered_radio_groups(driver)
    dropdown_changed, dropdown_skipped = fill_placeholder_dropdowns(driver)

    print("\n--- Summary ---")
    print(f"Radio groups changed: {radio_changed}")
    print(f"Dropdowns changed:   {dropdown_changed}")
    print(f"Items skipped:       {radio_skipped + dropdown_skipped}")
    print("Comments were left untouched.")
    print("Nothing was submitted. Review the page in Chrome.")


def main():
    try:
        driver = webdriver.Chrome()
    except WebDriverException as exc:
        print("Could not start Chrome through Selenium.")
        print("Update Chrome and run: py -m pip install --upgrade selenium")
        print(f"Details: {exc}")
        return

    driver.maximize_window()

    try:
        driver.get(SLCM_URL)
        input(
            "\nLog in manually and open one pending feedback questionnaire. "
            "\nWhen the questions are visible, return here and press Enter..."
        )

        while True:
            fill_current_questionnaire(driver)

            action = input(
                "\nReview the answers and submit the form yourself if appropriate. "
                "\nThen navigate manually to the next questionnaire. "
                "\nType NEXT when it is open, or QUIT to finish: "
            ).strip().upper()

            if action != "NEXT":
                break

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
