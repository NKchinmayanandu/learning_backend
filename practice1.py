import sys
import os
sys.path.append(os.path.dirname(os.path.abspath()))
from apps.services.user_services import get_user

print(get_user(1))
print(get_user(1))