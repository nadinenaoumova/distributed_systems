import time
import redis
from flask import Flask

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

def get_free_places():
    retries = 5

    while True:
        try:
            if not cache.exists('places'):
                cache.set('places', 1000)

            return cache.decr('places')

        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc

            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():

    places = get_free_places()

    return '''
    <h1 style="color:green">
        Конференция
    </h1>

    <p>
        Свободных мест:
        <strong>{}</strong>
    </p>
    '''.format(places)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
