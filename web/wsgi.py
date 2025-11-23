from app import app as application

# You can add any production-specific configurations here if needed
application.config['DEBUG'] = False 

if __name__ == "__main__":
    application.run()