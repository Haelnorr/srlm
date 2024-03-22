# Used to set the values of the permissions flags. Edit the variable names to suit your uses
class Permissions:
    none = 0
    superuser = 0b1
    admin = 0b10
    unusedperm_1 = 0b100
    unusedperm_2 = 0b1000
    unusedperm_3 = 0b10000
    unusedperm_4 = 0b100000
    unusedperm_5 = 0b1000000
    unusedperm_6 = 0b10000000
    unusedperm_7 = 0b100000000


PERMISSIONS = Permissions()

# NOTE: Variable names and labels should also be set in the following files:
# EditUserForm and AddUserForm classes in /lds/app/auth/forms.py
# get_permissions and list_permissions functions of the User class in /lds/app/models.py
# edit_user and add_user functions in /lds/app/auth/routes.py
# The templates edit_user.html and manage_users.html in /lds/app/templates/auth