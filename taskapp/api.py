from tastypie.resources import ModelResource
from taskapp.models import Task
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields
from taskapp.authorization import TaskAuthorization

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username']
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            "username":('exact', 'startswith')
        }

class TaskResource(ModelResource):
    creator = fields.ForeignKey(UserResource, attribute='creator',null=True, full=True)
    assigned_to = fields.ToManyField(UserResource, attribute='assigned_to', null=True,blank=True, full=True)
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        authentication = ApiKeyAuthentication()
        authorization = TaskAuthorization()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bundle = self.full_hydrate(bundle)    
        return super(TaskResource, self).obj_create(bundle, creator=bundle.request.user) 
