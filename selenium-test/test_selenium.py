from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import time
import os


BASE_URL = "http://localhost:8080"  # адрес твоего сервиса
NEW_CITY = "London"
EDGE_DRIVER_PATH = r"C:\practice_DTO\msedgedriver.exe"
def test_weather_city_change():
    # Инициализация Edge вместо Chrome
    service = EdgeService(executable_path=EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service)
    wait = WebDriverWait(driver, 10)

    # Папка для скриншотов (можно поменять путь)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SCREEN_DIR = os.path.join(BASE_DIR, "screenshots")
    os.makedirs(SCREEN_DIR, exist_ok=True)

    try:
        # 1. Открываем страницу
        driver.get(BASE_URL)
        driver.save_screenshot(os.path.join(SCREEN_DIR, "01_initial_page.png"))

        # 2. Читаем текущие значения в таблице
        city_cell = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "table.weather-table tbody tr td:nth-child(1)")
            )
        )
        temp_cell = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "table.weather-table tbody tr td:nth-child(2)")
            )
        )

        initial_city = city_cell.text
        initial_temp = temp_cell.text

        table = driver.find_element(By.CSS_SELECTOR, "table.weather-table")
        table.screenshot(os.path.join(SCREEN_DIR, "02_initial_table.png"))

        # 3. Вводим новый город
        city_input = wait.until(
            EC.element_to_be_clickable((By.ID, "city-input"))
        )
        city_input.clear()
        city_input.send_keys(NEW_CITY)

        driver.save_screenshot(os.path.join(SCREEN_DIR, "03_city_typed.png"))

        # 4. Нажимаем кнопку "Показать"
        submit_btn = driver.find_element(By.CSS_SELECTOR, "form.city-form button[type='submit']")
        submit_btn.click()

        # 5. Ждём обновления таблицы
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "table.weather-table tbody tr td:nth-child(1)"),
                NEW_CITY,
            )
        )

        new_city = driver.find_element(
            By.CSS_SELECTOR, "table.weather-table tbody tr td:nth-child(1)"
        ).text
        new_temp = driver.find_element(
            By.CSS_SELECTOR, "table.weather-table tbody tr td:nth-child(2)"
        ).text

        driver.save_screenshot(os.path.join(SCREEN_DIR, "04_after_change_full.png"))
        table = driver.find_element(By.CSS_SELECTOR, "table.weather-table")
        table.screenshot(os.path.join(SCREEN_DIR, "05_after_change_table.png"))

        # 6. Ассерты
        assert new_city == NEW_CITY, f"Ожидали город {NEW_CITY}, а видим {new_city}"
        assert new_temp != "", "Температура не должна быть пустой"
        assert (new_city != initial_city) or (new_temp != initial_temp), \
            "После смены города данные в таблице не изменились"

    except Exception as e:
        driver.save_screenshot(os.path.join(SCREEN_DIR, "99_error.png"))
        raise e

    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    test_weather_city_change()
