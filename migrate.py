import os
print('Making migrations for Series:')
os.system('python manage.py makemigrations qualitytracker')

print('\n\nCreating migrations:')
os.system('python manage.py migrate')

input("Press Enter to continue...")