import io 
import unittest
import pandas as pd
from app import app

class FlaskIntegrationTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_add_remove_todos_and_download_excel(self):
        for i in range(1,6):
            self.client.post('/add', data={
                'todo': f'Todo {i}'
            })

        self.client.get('/remove/2')

        response = self.client.get('/download_todos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') #ensure the content type is correct (excel)

        with io.BytesIO(response.data) as buffer:
            df = pd.read_excel(buffer, engine='openpyxl')

            self.assertListEqual(['Todo 1', 'Todo 3', 'Todo 4', 'Todo 5'], df.todo.values.tolist()) #ensure the todos are correct df['Todos'].tolist()


if __name__ == '__main__':
    client = FlaskIntegrationTest()
    client.setUp()
    client.test_add_remove_todos_and_download_excel()