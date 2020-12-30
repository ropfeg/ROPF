"""
WSGI config for ROPF_Main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# print("Hello")
# activator = 'D:\Django_20_feb_2020\\venv\Scripts\\activate_this.py'  # Looted from virtualenv; should not require modification, since it's defined relatively
# with open(activator) as f:
#     exec(f.read(), {'__file__': activator})
# @background(schedule=1)
# def backup():
#     print("backup done")
#     return
# backup()
print("Startmod")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ROPF_Main.settings')
print("Start2")
application = get_wsgi_application()
print("End")

# import sched, time
# s = sched.scheduler(time.time, time.sleep)
# def do_something(sc):
#     print("Doing stuff...")
#     # do your stuff
#     s.enter(60, 1, do_something, (sc,))
#
# s.enter(60, 1, do_something, (s,))
# s.run()
