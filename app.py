
# import the create app function from __init__.py
from website import create_app

# run create app function as main
if __name__=="__main__":
    app = create_app()
    app.run(debug=True)