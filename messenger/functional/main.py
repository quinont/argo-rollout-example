import requests
import unittest
import json
import time
from concurrent.futures import ThreadPoolExecutor


class TestAPI(unittest.TestCase):

    def setUp(self):
        #with open('config.json') as json_file:
        #    self.config = json.load(json_file)
        #self.base_url = self.config['base_url']
        #self.headers = self.config['headers']
        self.base_url = "http://localhost:8080/message"
        self.headers = {"Content-Type": "application/json"}

    def make_request(self):
        start_time = time.time()
        response = requests.get(self.base_url, headers=self.headers)
        duration = time.time() - start_time
        return response.status_code, duration, response.json()

    def test_get_request(self):
        response_status, _, _ = self.make_request()
        self.assertEqual(response_status, 200)

    def test_parallel_requests(self):
        num_requests = 20
        num_success = 0
        num_server_error = 0
        total_time = 0

        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(self.make_request)
                       for _ in range(num_requests)]

        for future in futures:
            status_code, duration, _ = future.result()
            total_time += duration

            if status_code == 200:
                num_success += 1
            elif status_code == 500:
                num_server_error += 1

        success_rate = num_success / num_requests
        avg_response_time = total_time / num_requests

        print(f"success rate: {success_rate}")
        print(f"avg response time: {avg_response_time}")

        # Asegurarse de que al menos el 80% de las solicitudes sean exitosas
        self.assertGreaterEqual(success_rate, 0.8, "El porcentaje de solicitudes exitosas es menor al 80%")

        # Asegurarse de que el tiempo promedio de respuesta no sea mayor a 200 ms
        self.assertLessEqual(avg_response_time, 0.2, "El tiempo promedio de respuesta supera los 200 ms")


    def test_post_request(self):
        data = {"new_msg": "nuevo mensaje"}
        status_code_esperado_post = 200
        respuesta_esperada = {"msg": "nuevo mensaje"}
        response = requests.post(self.base_url, headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, status_code_esperado_post)

        response_status, _, response_json = self.make_request()
        print(f"Status de Respuesta: {response_status}")
        self.assertEqual(response_status, 200)
        print(f"Respuesta obtenida: {response_json}")
        print(f"Respuesta esperada: {respuesta_esperada}")
        self.assertEqual(response_json, respuesta_esperada, "La respuesta no es igual")


if __name__ == '__main__':
    unittest.main()
