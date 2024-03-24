# keeping this file around only until password reset functionality implemented

"""@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Token is invalid or expired. Try again or contact an administrator')
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        if not form.new_password.data == form.confirm_password.data:
            flash("Passwords don't match")
            return redirect(url_for('auth.reset_password', token=token))
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('auth.login'))
    return make_response(render_template('auth/reset_password.html', app_name=app_name, page='Reset Password', form=form))
"""
