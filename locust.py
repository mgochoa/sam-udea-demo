from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    host = 'https://nrihhcw8b7.execute-api.us-east-1.amazonaws.com/Prod'

    @task
    def index(self):
        self.client.get("/")
