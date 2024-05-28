class New():
	def __init__(self):
		self.a = 15



num = New()
# print(num.a)











# @action(detail=False, methods=['get'], url_path='test')
# def test(self, request):
#     # get current user profile
#     user = User.objects.get(username='user2')
#     profile = UserProfile.objects.get(user=user)
#     serializer = UserProfileSerializer(profile)
#     print(user.shared_workspaces.all())
#     return Response(serializer.data)

class Home():
    def __init__(self, a):
        self.a = a
    
    def add(self, b):
        return self.a + b


new = Home(5)
