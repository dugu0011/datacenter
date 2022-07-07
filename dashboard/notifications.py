from dashboard.models import Notif
def get_notifications(request):
    if request.user.is_authenticated:
        all_notifications = Notif.objects.filter(user=request.user, is_delete=False).order_by("-date")[:3]
        count = Notif.objects.filter(user=request.user, is_delete=False, is_read=False).count()
        return {
            'notifications':all_notifications, 'count':count
        }
    else:
        return {
            'notification':'no'
        }
