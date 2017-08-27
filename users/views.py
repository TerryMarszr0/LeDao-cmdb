# -*- coding: utf-8 -*-
from home.views import IndexPageView
from public.base import PublicView
from asset.models import Room
from users.models import Menu


class UserPageView(PublicView):
    template_name = 'user/user.html'

    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data(**kwargs)
        context['state'] = Room.STATE
        context['header_title'] = u'查看用户'
        context['path1'] = u'用户管理'
        context['path2'] = u'查看应用'
        return context

class MyInfoPageView(PublicView):
    template_name = 'user/my_info.html'

    def get_context_data(self, **kwargs):
        context = super(MyInfoPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'我的个人信息'
        context['path1'] = u'用户管理'
        context['path2'] = u'我的个人信息'
        return context

# ---------------------------------------------------分割线----------------------------------------------------------
class MenuPageView(PublicView):
    template_name = 'user/menu.html'

    def get_context_data(self, **kwargs):
        context = super(MenuPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'系统管理'
        context['path1'] = u'系统管理'
        context['path2'] = u'查看菜单'
        return context
# ---------------------------------------------------分割线-------------------------------------------------------------
class GroupMenuPageView(PublicView):
    template_name = 'user/group_menu.html'

    def get_context_data(self, **kwargs):
        context = super(GroupMenuPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'系统管理'
        context['path1'] = u'系统管理'
        context['path2'] = u'角色管理'
        context['all_menus'] = Menu.objects.all()       # 向前端传递数据
        return context
# ---------------------------------------------------分割线-------------------------------------------------------------


