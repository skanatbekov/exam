from flask_login import UserMixin
from flask_wtf import FlaskForm
import wtforms as wf

from . import app, db
from .models import Position, Employee, User


def position_choices():
    choices = []
    with app.app_context():
        positions = Position.query.all()
        for position in positions:
            choices.append((position.id, position.name))
    return choices


def negative_validator(form, field):
    if field.data < 0.0:
        raise wf.ValidationError('Значение не должно быть отрицательным.')


class PositionForm(FlaskForm):
    name = wf.StringField(label='Название должности', validators=[
        wf.validators.DataRequired()])
    department = wf.StringField(label='Отдел', validators=[
        wf.validators.DataRequired()])
    wage = wf.IntegerField(label='Заработная плата', validators=[
        wf.validators.DataRequired(),
        negative_validator])


def validate_inn_numbers(form, field):
    if field.data[0] not in ['1', '2']:
        raise wf.ValidationError('Значение должно начинаться на числа 1 или 2')


class EmployeeUpdateForm(FlaskForm):
    name = wf.StringField(label='ФИО сотрудника', validators=[
        wf.validators.DataRequired()])
    inn = wf.StringField(label='ИНН', validators=[
        wf.validators.DataRequired(),
        validate_inn_numbers,
        wf.validators.Length(min=14, max=14)])
    position_id = wf.SelectField(label='Должность', choices=position_choices)


class EmployeeForm(EmployeeUpdateForm):
    name = wf.StringField(label='ФИО сотрудника', validators=[
        wf.validators.DataRequired()])
    inn = wf.StringField(label='ИНН', validators=[
        wf.validators.DataRequired(),
        validate_inn_numbers,
        wf.validators.Length(min=14, max=14)])
    position_id = wf.SelectField(label='Должность', choices=position_choices)

    def validate_inn(self, field):
        if Employee.query.filter_by(inn=field.data).count() > 0:
            raise wf.ValidationError('Сотрудник с данным инн уже существует')


class UserLoginForm(FlaskForm):
    username = wf.StringField(label='Логин', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=20)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate_password(self, field):
        if len(field.data) < 8:
            raise wf.ValidationError('Длина пароля должна быть минимум 8 символов')


class UserRegisterForm(UserLoginForm):
    password_2 = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate(self, *args, **kwargs):
        if not super().validate(*args, **kwargs):
            return False
        if self.password.data != self.password_2.data:
            self.password_2.errors.append('Пароли должны совпадать')
            return False
        return True

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise wf.ValidationError('Пользователь с таким логином уже существует')