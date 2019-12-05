import os
print('\n\nCreating a superuser:')
os.system('python manage.py createsuperuser --username admin')

input("Press Enter to continue...")