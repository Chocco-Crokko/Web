from fl_askapp.models import Tag, Profile


def tags(request):
	popular_tags = Tag.objects.get_popular_tags()
	return {'popular_tags' : popular_tags}

def users(request):
    best_users = Profile.objects.best_users()[0:5]
    return {'best_users' : best_users}


