from app import app
from app.view.FileView import FileViewApp
from app.view.UserView import UserApp
from app.view.SearchView import SearchApp

app.register_blueprint(FileViewApp, url_prefix='/file_view')
app.register_blueprint(UserApp, url_prefix='/user')
app.register_blueprint(SearchApp, url_prefix='/search')