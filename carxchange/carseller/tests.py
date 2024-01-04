# Для роботи з теками
import os
# Тестові модулі Django
from django.core.files import File
from django.test import TestCase, LiveServerTestCase
# Тестові модулі Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# Тестові модулі Django REST Framework
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
# Функція для генерації строки, в'юшки API, моделі
from .funcs import generate_string
from .api.views import car_list, car_detail
from .models import Car
from users.models import CarUser

# Тести з Selenium
# Тест головної сторінки
class HostTest(LiveServerTestCase):
    def testhomepage(self):
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:8000/")
        assert "Car-X-change" in driver.title

# Тест можливості логіну
class LoginTest(LiveServerTestCase):
    def testlogin(self):
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:8000/users/login/")

        user_name_field = driver.find_element("name", "username")
        password_field = driver.find_element("name", "password")
        submit_button = driver.find_element("id", "login_submit_button")

        user_name_field.send_keys("oataman")
        password_field.send_keys("HunterS123F)(")
        submit_button.send_keys(Keys.RETURN)

        assert "Олег Атаман" in driver.page_source

# Тест реєстрації
class RegisterTest(LiveServerTestCase):
    def testregister(self):
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:8000/users/register/")

        username = generate_string()
        password = generate_string()
        full_name = generate_string()
        contacts = generate_string()
        region = "KYI"
        image = os.getcwd()+"\image.png" # Шлях до фотографії

        user_name_field = driver.find_element("name", "username")
        password_enter_field = driver.find_element("name", "password1")
        password_confirm_field = driver.find_element("name", "password2")
        full_name_field = driver.find_element("name", "full_name")
        contact_field = driver.find_element("name", "contacts")
        region_field = Select(driver.find_element("name", "region"))
        picture_field = driver.find_element("name", "picture")
        submit_button = driver.find_element("id", "register_submit_button")

        user_name_field.send_keys(username)
        password_enter_field.send_keys(password)
        password_confirm_field.send_keys(password)
        full_name_field.send_keys(full_name)
        contact_field.send_keys(contacts)
        region_field.select_by_value(region)
        picture_field.send_keys(image)
        submit_button.send_keys(Keys.RETURN)

        # Нас має перекинути на профіль користувача
        assert "full_name" in driver.page_source
        assert "contacts" in driver.page_source


# Тестування API
class APITest(APITestCase):
    # Початкові налаштування
    def setUp(self):
        # Генеруємо та зберігаємо окремі поля для подальшого порівняння
        self.firstcarname = generate_string()
        self.secondcarcolor = generate_string()
        self.userfullname = generate_string()
        # Генеруємо решту полів та створюємо об'єкти
        user = CarUser(
            username = 'testuser',
            password = 'testpassword',
            full_name = self.userfullname,
            region = 'KYI',
            contacts = generate_string(),
        )           
        user.picture.save(generate_string()+'.png', File(open('D:\\projects\\CarXChange\\carxchange\\media\\profile_pictures\\sellersample.jpeg', 'rb')))
        self.user = user # Зберігаємо об'єкт користувача
        car1 = Car(
            title = self.firstcarname,
            price = 333.3,
            runtime = 110.22,
            color = generate_string(),
            wheel = 'FRO',
            fuel = 'PET',
            accidents = 'POS',
            brand = 'BMW',
            transmission = 'MEC',
            description = generate_string(),
            owner = user
        )
        car2 = Car(
            title = generate_string(),
            price = 3232,
            runtime = 1320.22,
            color = self.secondcarcolor,
            wheel = 'FUL',
            fuel = 'ELE',
            accidents = 'NEG',
            brand = 'TOY',
            transmission = 'AUT',
            description = generate_string(),
            owner = user
        )
        car1.picture.save(generate_string()+'.png', File(open(os.getcwd()+"/image.png", 'rb')))
        car2.picture.save(generate_string()+'.png', File(open(os.getcwd()+"/image.png", 'rb')))

        # Об'єкт Django REST Framework factory для тестування більш складних методів
        self.factory = APIRequestFactory()
        # Посилання та в'юшки для тестування більш складних методів
        self.view_create = car_list 
        self.url_create = 'http://127.0.0.1:8000/api/cars/'
        self.view_delete = car_detail
        self.url_delete = 'http://127.0.0.1:8000/api/car/1/'

    # Тестування переліку машин (метод GET)
    def testcars(self):
        response = self.client.get("http://127.0.0.1:8000/api/cars/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['title'], self.firstcarname)
        self.assertEqual(response.data['data'][1]['color'], self.secondcarcolor)

    # Тестування переліку користувачів
    def testusers(self):
        response = self.client.get("http://127.0.0.1:8000/api/users/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['full_name'], self.userfullname)

    # Тестування сторінки окремої машини (метод GET)
    def testcar(self):
        response = self.client.get("http://127.0.0.1:8000/api/car/2/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['color'], self.secondcarcolor)

    # Тестування сторінки окремого користувача (метод GET)
    def testuser(self):
        response = self.client.get("http://127.0.0.1:8000/api/user/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['full_name'], self.userfullname)

    # Тестування сторінки окремого користувача (метод PUT)
    def testedituser(self):
        newname = generate_string()
        force_authenticate(self.client, user=self.user) # Авторизуємось
        response = self.client.get("http://127.0.0.1:8000/api/user/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['full_name'], self.userfullname)
        response = self.client.put("http://127.0.0.1:8000/api/user/1/", {'full_name':newname}) # Змінюємо ім'я
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], newname)

    # Тестування Сторінки окремої машини (метод PUT)
    def testeditcar(self):
        newname = generate_string()
        force_authenticate(self.client, user=self.user)
        response = self.client.get("http://127.0.0.1:8000/api/car/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['title'], self.firstcarname)
        response = self.client.put("http://127.0.0.1:8000/api/car/1/", {'title':newname}) # Пробуємо
        self.assertEqual(response.status_code, 405) # Метод заборонено

    # Тестування списку машин (метод POST) / Успішне створення
    def testcarcreate_good(self):
        ctx = {
            'title':self.firstcarname,
            'price':333.3,
            'runtime':110.22,
            'color':generate_string(),
            'wheel':'FRO',
            'fuel':'PET',
            'accidents':'POS',
            'brand':'BMW',
            'transmission':'MEC',
            'description':generate_string(),
            'picture':  File(open('D:\\projects\\CarXChange\\carxchange\\media\\profile_pictures\\sellersample.jpeg', 'rb'))
        }
        request = self.factory.post(self.url_create, ctx) # Створюємо запит
        force_authenticate(request, self.user) # Логінимось
        response = self.view_create(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], self.firstcarname) # Перевіряємо дані

    # Тестування списку машин (метод POST) / Створення заборонене
    def testcarcreate_bad(self):
        ctx = {
            'title':self.firstcarname,
            'price':333.3,
            'runtime':110.22,
            'color':generate_string(),
            'wheel':'FRO',
            'fuel':'PET',
            'accidents':'POS',
            'brand':'BMW',
            'transmission':'MEC',
            'description':generate_string(),
            'picture':  File(open('D:\\projects\\CarXChange\\carxchange\\media\\profile_pictures\\sellersample.jpeg', 'rb'))
        }
        request = self.factory.post(self.url_create, ctx) # Створюємо запит
        response = self.view_create(request) # Але не логінимось
        self.assertEqual(response.status_code, 403) # Створення заборонене

    # Перевірка сторінки окремої машини (метод DELETE) / Видалення заборонене
    def testdeletecar_bad(self):
        request = self.factory.delete(self.url_delete)
        response = self.view_delete(request, 1) # Не логінимось
        self.assertEqual(response.status_code, 403)

    # Перевірка сторінки окремої машини (метод DELETE) / Успішне видалення
    def testdeletecar_good(self):
        request = self.factory.delete(self.url_delete)
        force_authenticate(request, self.user) # Авторизація
        response = self.view_delete(request, 1)
        self.assertEqual(response.status_code, 200)


# Загальне тестування доступності вебсайту
class BaseTesting(TestCase):
    def setUp(self):
        # Створюємо об'єкти та зберігаємо поля для перевірки
        self.firstcarname = generate_string()
        self.secondcarcolor = generate_string()
        self.userfullname = generate_string()
        user = CarUser(
            username = 'testuser',
            password = 'testpassword',
            full_name = self.userfullname,
            region = 'KYI',
            contacts = generate_string(),
        )           
        user.picture.save(generate_string()+'.png', File(open('D:\\projects\\CarXChange\\carxchange\\media\\profile_pictures\\sellersample.jpeg', 'rb')))
        self.user = user
        car1 = Car(
            title = self.firstcarname,
            price = 333.3,
            runtime = 110.22,
            color = generate_string(),
            wheel = 'FRO',
            fuel = 'PET',
            accidents = 'POS',
            brand = 'BMW',
            transmission = 'MEC',
            description = generate_string(),
            owner = user
        )
        car2 = Car(
            title = generate_string(),
            price = 3232,
            runtime = 1320.22,
            color = self.secondcarcolor,
            wheel = 'FUL',
            fuel = 'ELE',
            accidents = 'NEG',
            brand = 'TOY',
            transmission = 'AUT',
            description = generate_string(),
            owner = user
        )
        car1.picture.save(generate_string()+'.png', File(open(os.getcwd()+"/image.png", 'rb')))
        car2.picture.save(generate_string()+'.png', File(open(os.getcwd()+"/image.png", 'rb')))

    # Тестування головної сторінки
    def testhome(self):
        response = self.client.get("http://127.0.0.1:8000/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carseller/index.html')

    # Тестування списку машин
    def testcars(self):
        response = self.client.get("http://127.0.0.1:8000/cars")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carseller/cars.html')

    # Тестування списку продавців
    def testusers(self):
        response = self.client.get("http://127.0.0.1:8000/sellers")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carseller/sellers.html')

    # Тестування сторінки окремої машини
    def testonecar(self):
        response = self.client.get("http://127.0.0.1:8000/car/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carseller/carview.html')

    # Тестування сторінки окремого продавця
    def testoneseller(self):
        response = self.client.get("http://127.0.0.1:8000/seller/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carseller/seller.html')

    # Тестування видалення машини (Заборонене)
    def testdeletecar(self):
        response = self.client.delete("http://127.0.0.1:8000/deletecar/1")
        self.assertEqual(response.status_code, 403)