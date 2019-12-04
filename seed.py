import os
print('\n\nSeeding the database with example data:')
os.system('python manage.py loaddata seed.json')

input("Press Enter to continue...")