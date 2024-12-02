from dotenv import load_dotenv
load_dotenv()  

import os
from mike_x_webhook_server import create_app

app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
    print("hello")