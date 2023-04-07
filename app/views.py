from flask import request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required

from app import db
from .models import Position, Employee, User
from .forms import PositionForm, EmployeeForm, EmployeeUpdateForm, UserRegisterForm, UserLoginForm


def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


@login_required
def position_create():
    form = PositionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_position = Position()
            form.populate_obj(new_position)
            db.session.add(new_position)
            db.session.commit()
            flash('Должность успешно добавлена', 'Успешно!')
            return redirect(url_for('index'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении Должности произошла ошибка. {". ".join(text_list)}', 'Ошибка!')
    return render_template('form.html', form=form)


@login_required
def employee_create():
    form = EmployeeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_employee = Employee()
            form.populate_obj(new_employee)
            db.session.add(new_employee)
            db.session.commit()
            flash('Работник успешно добавлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении работника произошла ошибка. {". ".join(text_list)}', 'Ошибка!')
    return render_template('form.html', form=form)


@login_required
def employee_detail(employee_id):
    employee = Employee.query.get(employee_id)
    return render_template('employee_detail.html', employee=employee)


@login_required
def employee_update(employee_id):
    employee = Employee.query.get(employee_id)
    form = EmployeeUpdateForm(obj=employee)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('Работник успешно изменен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При изменении работника произошла ошибка. {". ".join(text_list)}', 'Ошибка!')

    return render_template('form.html', form=form)


@login_required
def employee_delete(employee_id):
    employee = Employee.query.get(employee_id)
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        flash('Работник успешно удален', 'Успешно!')
        return redirect(url_for('index'))
    return render_template('employee_delete.html', employee=employee)


def register():
    form = UserRegisterForm()
    title = 'Регистрация'
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {new_user.username} успешно зарегистрирован', 'Успех!')
            return redirect(url_for('login'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При регистрации произошла ошибка. {". ".join(text_list)}', 'Ошибка!')
    return render_template('user_form.html', form=form, title=title)


def login():
    form = UserLoginForm()
    title = 'Авторизация'
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему', 'Успех!')
                return redirect(url_for('index'))
            else:
                flash('Невеные логин и пароль', 'Ошибка!')
    return render_template('user_form.html', form=form, title=title)


def logout():
    logout_user()
    return redirect(url_for('login'))