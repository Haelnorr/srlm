from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList
from wtforms.validators import DataRequired, Email


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ForgotPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password')


class ResetPassword(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')


class ChangePassword(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')


class ChangeDetails(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Details')


# Edit the form below to make use of the permission flags
class EditUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    perm_admin = BooleanField('Admin')
    perm_unusedperm_1 = BooleanField('Unused1')
    perm_unusedperm_2 = BooleanField('Unused2')
    perm_unusedperm_3 = BooleanField('Unused3')
    perm_unusedperm_4 = BooleanField('Unused4')
    perm_unusedperm_5 = BooleanField('Unused5')
    perm_unusedperm_6 = BooleanField('Unused6')
    perm_unusedperm_7 = BooleanField('Unused7')
    reset_password = BooleanField('Reset Password')
    save = SubmitField('Save')
    delete = SubmitField('Delete')


# Edit the form below to make use of the permission flags
class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    perm_admin = BooleanField('Admin')
    perm_unusedperm_1 = BooleanField('Unused1')
    perm_unusedperm_2 = BooleanField('Unused2')
    perm_unusedperm_3 = BooleanField('Unused3')
    perm_unusedperm_4 = BooleanField('Unused4')
    perm_unusedperm_5 = BooleanField('Unused5')
    perm_unusedperm_6 = BooleanField('Unused6')
    perm_unusedperm_7 = BooleanField('Unused7')
    submit = SubmitField('Add User')


class ClearLogs(FlaskForm):
    clear = SubmitField('Clear')
