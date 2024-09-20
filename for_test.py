import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestFlaskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Установить путь к драйверу для Firefox
        cls.driver = webdriver.Firefox()

    def setUp(self):
        # Открыть страницу
        self.driver.get('http://127.0.0.1:5000') 

    def test_add_input_fields(self):
        # Проверка загрузки страницы
        self.assertIn("Главная страница", self.driver.title)

        # Добавление 5 полей
        add_input_button = self.driver.find_element(By.ID, 'add-input')
        for _ in range(5):
            add_input_button.click()
            sleep(1)

        # 2 секунды приостановки потока на обовление страницы
        sleep(2)

        # Подсчет количества полей
        inputs_container = self.driver.find_element(By.ID, 'inputs-container')
        inputs = inputs_container.find_elements(By.TAG_NAME, 'input')
        
        # Проверка количества полей, должно быть 6
        self.assertEqual(len(inputs), 6)  

        # Получаем все инпуты на странице и добавляем в них данные
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "#inputs-container input")
        for i in range(len(inputs)):
            inputs[i].send_keys(f"data{i + 1}")
            sleep(1)

        sleep(2)

        # Кликаем на кнопку отправки формы
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        # Ожидаем уведомление об успешной отправке данных
        alert = self.driver.switch_to.alert
        
        self.assertEqual(alert.text, 'Данные успешно отправлены!')
        sleep(3)
        alert.accept()  # Закрываем уведомление

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
