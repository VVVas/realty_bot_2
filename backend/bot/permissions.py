from functools import wraps

from django.core.exceptions import ObjectDoesNotExist

from users.models import Profile


def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        try:
            user_id = update.effective_user.id
            user_profile = Profile.objects.get(external_id=user_id)
            if user_profile and user_profile.is_blocked:
                print(f"Unauthorized access denied for {user_id}.")
                return None
            return await func(update, context, *args, **kwargs)
        except ObjectDoesNotExist:
            return await func(update, context, *args, **kwargs)
    return wrapped
