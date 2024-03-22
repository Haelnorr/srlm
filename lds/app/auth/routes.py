from sqlalchemy import delete
from flask import redirect, url_for, flash, render_template, make_response, abort
from flask_login import current_user, login_user, logout_user, login_required
from lds.logger import get_logger
from lds.definitions import PERMISSIONS, app_name
from lds.app import db
from lds.app.events import log_event
from lds.app.models import User, load_user
from lds.app.auth import bp
from lds.app.auth.forms import Login, ForgotPassword, ResetPassword, ChangePassword, ChangeDetails, AddUserForm, \
    EditUserForm
from lds.app.auth.email import send_password_reset_email, send_new_user_email
from lds.app.auth.functions import get_permissions, check_email_exists

log = get_logger(__name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    log.debug('Loading request for Login page')
    form = Login()
    if form.validate_on_submit():
        log.debug('Login attempted, querying data')

        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            log.debug('Invalid credentials, login failed')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        log.debug('Login successful, redirecting to Dashboard')
        return redirect(url_for('main.dashboard'))
    return make_response(render_template('auth/login.html', app_name=app_name, page='Login', form=form))


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = ForgotPassword()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            log_event(user, 'Auth', 'Requested password reset email')
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('auth.login'))
    return make_response(render_template('auth/forgot_password.html', app_name=app_name, page='Forgot Password', form=form))


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Token is invalid or expired. Try again or contact an administrator')
        return redirect(url_for('auth.login'))
    form = ResetPassword()
    if form.validate_on_submit():
        if not form.new_password.data == form.confirm_password.data:
            flash("Passwords don't match")
            return redirect(url_for('auth.reset_password', token=token))
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('auth.login'))
    return make_response(render_template('auth/reset_password.html', app_name=app_name, page='Reset Password', form=form))


@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        user = load_user(current_user.id)
        if user is None:
            flash('Some error occurred, try again and if the problem persists contact a system administrator')
            return redirect(url_for('auth.change_password'))
        if not user.check_password(form.old_password.data):
            flash('Old password incorrect')
            return redirect(url_for('auth.change_password'))
        if not form.new_password.data == form.confirm_password.data:
            flash("Passwords don't match")
            return redirect(url_for('auth.change_password'))
        user.set_password(form.new_password.data)
        user.reset_pass = False
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return make_response(render_template('auth/change_password.html', app_name=app_name, page='Change Password', form=form))


@login_required
@bp.route('/change_details', methods=['POST', 'GET'])
def change_details():
    log.debug('Getting current_user data from db')
    user = load_user(current_user.id)
    form = ChangeDetails()

    if form.validate_on_submit():
        log.debug('Submitted form data: Username - {}, Email - {}'.format(form.username.data, form.email.data))
        log.debug('User data from db: Username - {}, Email - {}'.format(user.username, user.email))
        # check username is unique
        log.debug('Checking if user data has been changed')
        old_username = user.username
        new_username = form.username.data
        old_email = user.email
        new_email = form.email.data
        username_changed = False
        email_changed = False

        if not new_username == old_username:
            log.debug('Username has been changed')
            username_changed = True
            log.debug('Checking new username is unique')
            username_query = db.session.query(User).filter(User.username == new_username)
            username_exists = db.session.query(username_query.exists()).scalar()
            if username_exists:
                # username is not unique
                log.debug('Username is not unique, reloading form')
                flash('Username is taken, please use a different username')
                return redirect(url_for('auth.change_details'))

            # username valid
            log.debug('Username is unique')
            user.username = new_username

        if not new_email == old_email:
            log.debug('Email has been updated by user')
            email_changed = True
            # check email is unique
            email_query = db.session.query(User).filter(User.email == new_email)
            email_exists = db.session.query(email_query.exists()).scalar()
            if email_exists:
                # email is not unique
                log.debug('Email is not unique, reloading form')
                flash('Email is already associated with an account')
                return redirect(url_for('auth.change_details'))

            # email valid
            log.debug('Email is unique')
            user.email = new_email

        if username_changed or email_changed:
            log.debug('User data has been validated, updating database')
            db.session.add(user)
            db.session.commit()
            log.debug('Re-logging user')
            logout_user()
            login_user(user, remember=False)

        if username_changed:
            log_event(current_user, 'Auth', 'Changed username. Old: {}, New: {}'.format(old_username, new_username))

        if email_changed:
            log_event(current_user, 'Auth', 'Changed email. Old: {} New: {}'.format(old_email, new_email))

        log.debug('Form submitted successfully, redirecting to dashboard')
        return redirect(url_for('main.dashboard'))
    log.debug('Populating form with user data')
    form.username.data = user.username
    form.email.data = user.email
    log.debug('Rendering template')
    return make_response(render_template('auth/change_details.html', app_name=app_name, page='View/Change Details', form=form))


@login_required
@bp.route('/manage')
def manage_users():
    users = db.session.query(User).all()
    permissions = get_permissions(current_user.id)
    if not permissions['admin']:
        abort(403)

    return make_response(
        render_template('auth/manage_users.html', app_name=app_name, page="Manage Users", permissions=permissions, users=users))


@login_required
@bp.route('/manage/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id=None):
    permissions = get_permissions(current_user.id)
    if not permissions['admin']:
        abort(403)

    if user_id is None:
        return redirect(url_for('auth.manage_users'))

    form = EditUserForm()
    user = load_user(user_id)
    user_perms = user.get_permissions()

    # check if form is submitted
    if form.validate_on_submit():
        if form.save.data:
            # user was updated
            log.debug('Form was saved')
            old_email = user.email
            new_email = form.email.data
            email_exists = False
            email_changed = False
            perms_changed = False

            # check if email has been changed
            if new_email != old_email:
                log.debug('Email has been changed, checking if unique')
                email_changed = True
                email_exists = check_email_exists(new_email)
            # check if email is unique (if changed)
            if email_exists:
                log.debug('Email is not unique')
                flash('Email is already in use')
                return redirect(url_for('auth.edit_user', user_id=user_id))

            if email_changed:
                user.email = new_email

            # check if reset password was set and send email
            if form.reset_password.data:
                log.debug('Password reset selected, sending email to user')
                send_password_reset_email(user)
                log_event(current_user, 'Auth', 'Reset password for user: {}'.format(user.username))

            # update permissions
            old_perms = user.permissions
            new_perms = int(form.perm_admin.data) * PERMISSIONS.admin + \
                int(form.perm_unusedperm_1.data) * PERMISSIONS.unusedperm_1 + \
                int(form.perm_unusedperm_2.data) * PERMISSIONS.unusedperm_2 + \
                int(form.perm_unusedperm_3.data) * PERMISSIONS.unusedperm_3 + \
                int(form.perm_unusedperm_4.data) * PERMISSIONS.unusedperm_4 + \
                int(form.perm_unusedperm_5.data) * PERMISSIONS.unusedperm_5 + \
                int(form.perm_unusedperm_6.data) * PERMISSIONS.unusedperm_6 + \
                int(form.perm_unusedperm_7.data) * PERMISSIONS.unusedperm_7

            if new_perms != old_perms:
                user.permissions = new_perms
                log.debug('User permissions set')
                perms_changed = True

            if email_changed or perms_changed:
                log.debug('Updating user in database')
                db.session.add(user)
                db.session.commit()

            if email_changed:
                log_event(current_user, 'Auth', 'Updated email for user: {} - Old: {}, New: {}'.format(user.username, old_email, new_email))

            if perms_changed:
                log_event(current_user, 'Auth', 'Updated permission level for user: {} - Old: {}, New: {}'.format(user.username, old_perms, new_perms))

        if form.delete.data:
            log.debug('Deleting user {}'.format(user.username))
            db.session.execute(delete(User).where(User.id == user_id).execution_options(synchronize_session='fetch'))
            db.session.commit()
            log_event(current_user, 'Auth', 'Deleted user: {}'.format(user.username))

            return redirect(url_for('auth.manage_users'))

        return redirect(url_for('auth.edit_user', user_id=user_id))

    # loading user data from database into the form

    form.email.data = user.email
    form.perm_admin.data = user_perms['admin']
    form.perm_unusedperm_1.data = user_perms['unusedperm_1']
    form.perm_unusedperm_2.data = user_perms['unusedperm_2']
    form.perm_unusedperm_3.data = user_perms['unusedperm_3']
    form.perm_unusedperm_4.data = user_perms['unusedperm_4']
    form.perm_unusedperm_5.data = user_perms['unusedperm_5']
    form.perm_unusedperm_6.data = user_perms['unusedperm_6']
    form.perm_unusedperm_7.data = user_perms['unusedperm_7']

    return make_response(render_template('auth/edit_user.html', app_name=app_name, page='Edit User', user=user, form=form))


@login_required
@bp.route('/manage/add', methods=['GET', 'POST'])
def add_user():
    permissions = get_permissions(current_user.id)
    if not permissions['manage_users']:
        abort(403)

    form = AddUserForm()

    # check if form is submitted
    if form.validate_on_submit():
        log.debug('Form submitted')
        # check data is valid
        query = db.session.query(User)
        username_exists = db.session.query(query.filter(User.username == form.username.data).exists()).scalar()
        email_exists = db.session.query(query.filter(User.email == form.email.data).exists()).scalar()
        if username_exists:
            log.debug('Username taken')
            flash('Username taken, enter a different username')
        if email_exists:
            log.debug('Email taken')
            flash('Email already in use, enter a different email')
        if username_exists or email_exists:
            log.debug('Data not unique, reloading form')
            return redirect(url_for('auth.add_user'))

        # user details verified
        user = User.new(form.username.data, form.email.data, None)
        # add permissions
        if form.perm_admin.data:
            user.add_permission(PERMISSIONS.admin)
        if form.perm_unusedperm_1.data:
            user.add_permission(PERMISSIONS.unusedperm_1)
        if form.perm_unusedperm_2.data:
            user.add_permission(PERMISSIONS.unusedperm_2)
        if form.perm_unusedperm_3.data:
            user.add_permission(PERMISSIONS.unusedperm_3)
        if form.perm_unusedperm_4.data:
            user.add_permission(PERMISSIONS.unusedperm_4)
        if form.perm_unusedperm_5.data:
            user.add_permission(PERMISSIONS.unusedperm_5)
        if form.perm_unusedperm_6.data:
            user.add_permission(PERMISSIONS.unusedperm_6)
        if form.perm_unusedperm_7.data:
            user.add_permission(PERMISSIONS.unusedperm_7)

        log.debug('User details updated')
        log.debug('Adding user to database')

        db.session.add(user)
        db.session.commit()
        log_event(current_user, 'Auth', 'Added a new user'.format(user.username))
        log.debug('User added, reloading user from database to get ID and send email')
        log.debug('User added to database')

        user = db.session.query(User).filter(User.username == user.username).first()
        send_new_user_email(user)
        log.debug('Sent welcome email to user')

        return redirect(url_for('auth.manage_users'))

    return make_response(render_template('auth/add_user.html', app_name=app_name, page="Add User", form=form))


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.dashboard'))
