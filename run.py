from project import create_app
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == '__main__':
  app = create_app()
  app.run(host = os.getenv('LOCALHOST'), port = os.getenv('PORT'), debug=os.getenv('DEBUG'))


