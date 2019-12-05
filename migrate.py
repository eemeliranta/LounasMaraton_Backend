import os
print('Making migrations:')
os.system('python manage.py makemigrations backend')

print('\n\nCreating migrations:')
os.system('python manage.py migrate')

input("Press Enter to continue...")