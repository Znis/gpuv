from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from gpuv.models import UserVm

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        # session.delete()
        data = session.get_decoded()
        uid = data.get('_auth_user_id', None)
        if uid is not None and uid not in uid_list:
            uid_list.append(uid)

    # Query all logged in users based on id list
    return uid_list


def isVmFree(requested_user):
    current_requestedvm = UserVm.objects.filter(user_choice_id = requested_user).values()[0]['vm_choice_id']
    authUsersList = get_all_logged_in_users()
    for authUser in authUsersList:
      
        if requested_user == int(authUser):
            return True, False
        if UserVm.objects.filter(user_choice_id = authUser).values()[0]['vm_choice_id'] == current_requestedvm:
            return False, False
        
    return False, True #is_same_user False , is_vm_free True
   

