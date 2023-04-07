from . import app, db
from . import views


app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/position/create', view_func=views.position_create, methods=['GET', 'POST'])
app.add_url_rule('/employee/create', view_func=views.employee_create, methods=['GET', 'POST'])
app.add_url_rule('/employee/<int:employee_id>/update', view_func=views.employee_update, methods=['POST', 'GET'])

app.add_url_rule('/employee/<int:employee_id>/detail', view_func=views.employee_detail)
app.add_url_rule('/employee/<int:employee_id>/delete', view_func=views.employee_delete, methods=['POST', 'GET'])


app.add_url_rule('/register', view_func=views.register, methods=['POST', 'GET'])
app.add_url_rule('/login', view_func=views.login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=views.logout)