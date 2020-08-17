from django.db import models

'''用户类型表操作'''


class UserTypeManager(models.Manager):
    def insert_user_type(self, user_type):
        self.create(user_type=user_type)

    def insert_type_name(self, type_name):
        self.create(type_name=type_name)

    def insert_type_desc(self, type_desc):
        self.create(type_desc=type_desc)

    def get_objects(self, user_type_id):  # 根据user_type得到一条数据
        return self.get(user_type_id=user_type_id)


'''用户信息表操作'''


class UserInfoManager(models.Manager):
    def insert_user(self, username, password, email, object):
        self.create(username=username, password=password, email=email, user_type=object)

    def query_user(self, username, password):
        return self.filter(username__exact=username, password__exact=password).count()


'''项目信息表操作'''


class ProjectInfoManager(models.Manager):
    def insert_project(self, **kwargs):
        self.create(**kwargs)

    def update_project(self, id,user_account, **kwargs):  # 如此update_time才会自动更新！！
        obj = self.get(id=id,user_account=user_account)
        obj.project_name = kwargs.get('project_name')
        obj.responsible_name = kwargs.get('responsible_name')
        obj.test_user = kwargs.get('test_user')
        obj.dev_user = kwargs.get('dev_user')
        obj.publish_app = kwargs.get('publish_app')
        obj.simple_desc = kwargs.get('simple_desc')
        obj.other_desc = kwargs.get('other_desc')
        obj.user_account = user_account
        obj.save()

    def get_pro_name(self, pro_name,user_account, type=True, id=None):
        if type:
            return self.filter(project_name__exact=pro_name,user_account=user_account).count()
        else:
            if id is not None:
                return self.get(id=id,user_account=user_account).project_name
            return self.get(project_name__exact=pro_name,user_account=user_account)

    def get_pro_info(self,user_account, type=True):
        if type:
            return self.filter(user_account=user_account).all().values('project_name')
        else:
            return self.filter(user_account=user_account).all()


'''模块信息表操作'''


class ModuleInfoManager(models.Manager):
    def insert_module(self, **kwargs):
        self.create(**kwargs)

    def update_module(self,id, **kwargs):
        obj = self.get(id=id,user_account=kwargs.get('user_account'))
        obj.module_name = kwargs.get('module_name')
        obj.test_user = kwargs.get('test_user')
        obj.simple_desc = kwargs.get('simple_desc')
        obj.other_desc = kwargs.get('other_desc')
        obj.user_account = kwargs.get('user_account')
        obj.save()

    def get_module_name(self, module_name,user_account, type=True, id=None):
        if type:
            return self.filter(module_name__exact=module_name,user_account=user_account).count()
        else:
            if id is not None:
                return self.get(id=id,user_account=user_account).module_name
            else:
                return self.get(id=module_name,user_account=user_account)

    def get_module_by_id(self, index,user_account, type=True):
        if type:
            return self.filter(id=index,user_account=user_account).all()
        else:
            return self.get(id=index,user_account=user_account).name



'''用例信息表操作'''


class TestCaseInfoManager(models.Manager):
    def insert_case(self, belong_module, **kwargs):
        case_info = kwargs.get('test').pop('case_info')
        self.create(name=kwargs.get('test').get('name'), belong_project=case_info.pop('project'),
                    belong_module=belong_module,
                    author=case_info.pop('author'), include=case_info.pop('include'), request=kwargs.get('test'),
                    user_account=kwargs.get('user_account'))

    def update_case(self,belong_module, **kwargs):
        case_info = kwargs.get('test').pop('case_info')
        obj = self.get(id=case_info.pop('test_index'),user_account=kwargs.get('user_account'))
        obj.belong_project = case_info.pop('project')
        obj.belong_module = belong_module
        obj.name = kwargs.get('test').get('name')
        obj.author = case_info.pop('author')
        obj.include = case_info.pop('include')
        obj.request = kwargs.get('test')
        obj.user_account = kwargs.get('user_account')
        obj.save()

    def insert_config(self,belong_module, **kwargs):
        config_info = kwargs.get('config').pop('config_info')
        self.create(name=kwargs.get('config').get('name'), belong_project=config_info.pop('project'),
                    belong_module=belong_module,
                    author=config_info.pop('author'), type=2, request=kwargs,user_account=kwargs.get('user_account'))

    def update_config(self,belong_module, **kwargs):
        config_info = kwargs.get('config').pop('config_info')
        obj = self.get(id=config_info.pop('test_index'),user_account=kwargs.get('user_account'))
        obj.belong_module = belong_module
        obj.belong_project = config_info.pop('project')
        obj.name = kwargs.get('config').get('name')
        obj.author = config_info.pop('author')
        obj.request = kwargs
        obj.user_account = kwargs.get('user_account')
        obj.save()

    def get_case_name(self, name, module_name, belong_project,user_account):
        return self.filter(belong_module__id=module_name).filter(name__exact=name).filter(
            belong_project__exact=belong_project).filter(user_account=user_account).count()

    def get_case_by_id(self,index,user_account, type=True):
        if type:
            return self.filter(id=index,user_account=user_account).all()
        else:
            return self.get(id=index,user_account=user_account).name
    def get_case_by_moduleId(self,module_id,user_account,type=1,is_all=True):
        if is_all:
            return self.filter(belong_module=module_id,user_account=user_account).filter(type=type).all()
        else:
            return self.filter(belong_module=module_id,user_account=user_account).name



'''环境变量管理'''


class EnvInfoManager(models.Manager):
    def insert_env(self, **kwargs):
        self.create(**kwargs)

    def update_env(self, index, **kwargs):
        obj = self.get(id=index,user_account=kwargs.get('user_account'))
        obj.env_name = kwargs.pop('env_name')
        obj.base_url = kwargs.pop('base_url')
        obj.simple_desc = kwargs.pop('simple_desc')
        obj.user_account = kwargs.get('user_account')
        obj.save()

    def get_env_name(self,index,user_account):
        return self.get(id=index,user_account=user_account).env_name

    def delete_env(self,index,user_account):
        self.get(id=index,user_account=user_account).delete()
