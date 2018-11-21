# _*_ encoding:utf-8 _*_
from django.shortcuts import render, redirect, HttpResponse
from django.http import StreamingHttpResponse
from django import forms
from django.forms import fields
from django.forms import widgets
import random
from app import models
import json
from datetime import datetime
from my_form import docx,read_file
from result import datas as da


# Create your views here.
class User(forms.Form):
    # 登录界面的用户名框，error_messages为fields包的参数，输入为空时的提示，widget为该input标签的属性
    username = fields.CharField(error_messages={'required': '用户名不能为空'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    # 密码框的定制
    password = fields.CharField(error_messages={'required': '密码不能为空.'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"}))


class Newuser(forms.Form):
    # 注册界面用户名框最长长度不能超过9，最小不能小于3，且不能为空
    username = fields.CharField(max_length=9, min_length=3,
                                error_messages={'required': '用户名不能为空', 'max_length': '用户名长度不能大于9',
                                                'min_length': '用户名长度不能小于3'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    # 注册界面密码框最长长度不能超过12，最小不能小于6，且不能为空
    password = fields.CharField(max_length=12, min_length=6,
                                error_messages={'required': '密码不能为空.', 'max_length': '密码长度不能大于12',
                                                'min_length': '密码长度不能小于6'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"})
                                )
    # 注册界面再次输入密码框最长长度不能超过9，并与前一个密码框内容比较，两次不一致提示“两次密码不一致”，最小不能小于3，且不能为空
    confirm_password = fields.CharField(max_length=12, min_length=6,
                                        error_messages={'required': '不能为空.', 'max_length': '两次密码不一致',
                                                        'min_length': '两次密码不一致'},
                                        widget=widgets.Input(
                                            attrs={'type': "password", 'class': "form-control",
                                                   'name': "confirm_password",
                                                   'id': "confirm_password",
                                                   'placeholder': "请重新输入密码"})
                                        )


def login(request):
    """
        登陆
        :param request:
        :return:
        """
    # 定义空字符串，以便向前端页面提示错误
    s = ''
    # Get请求，返回login.html界面，输入框规则参照制定的User()并实列化
    if request.method == 'GET':
        obj = User()
        return render(request, 'login.html', {'obj': obj})
    # POST请求，通过实例化User()表单验证输入是否符合要求，并把用户名和密码提交到后端验证，
    # 与数据库比较是否存在该用户且密码正确，分别给出相应提示
    if request.method == 'POST':
        obj = User(request.POST)
        u = request.POST.get('username')
        t1 = models.User.objects.filter(username=u)
        if t1:
            pwd = request.POST.get('password')
            if pwd == t1[0].pwd:
                request.session['user'] = u
                request.session['is_login'] = True
                return redirect('/main/', )
            else:
                s = '''
                      <script>alert('密码错误!!!请重新输入!!!');</script>
                  '''
        # 输入的用户名不存在
        else:
            s = '''
               <script>alert('该用户名不存在!!!请检查是否正确!!!');</script>
                                    '''
        return render(request, 'login.html', {'obj': obj, 's': s})


def register(request):
    """
       注册
       :param request:
       :return:
       """
    # 定义空字符串，以便向前端页面提示错误
    er = ''
    # 如果是GET请求，实例化类Newuser(),即进行注册的表单验证
    if request.method == 'GET':
        obj = Newuser()
        return render(request, 'register.html', {'obj': obj, 'er': er})
    if request.method == 'POST':
        # form表单验证
        obj = Newuser(request.POST)
        # 该方法表示输入框的值是否都符合定制的规范，是则返回True，否则False
        r = obj.is_valid()
        if r:
            # 获取用户名框中内容并与数据库比较，若存在该用户，向像前端返回s，提示用户已经存在，不存在则继续验证
            user = request.POST.get('username')
            u = models.User.objects.filter(username=user)
            if u:
                s = '''
                       <script>alert('用户名已经存在，请从新输入用户名！');
                   </script>
                       '''
            else:
                # 验证输入框两次密码是否相同，不相同则提示不一致
                pwd1 = request.POST.get('password')
                pwd2 = request.POST.get('confirm_password')
                if pwd1 != pwd2:
                    s = '''
                           <script>alert('两次密码不一致，请核对重新输入！');</script>'''
                # 两次密码相同且用户不存在，注册成功，向前端提示成功
                else:
                    models.User.objects.create(username=user, pwd=pwd1)
                    s = '''
                           <script>alert('注册成功！');
                           </script>'''
            return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
            # 输入不符合定制的form表单验证，提示格式不正确
        else:
            s = '''
               <script>alert('信息格式不正确,注册失败！');
                   </script>'''
            return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})


def main(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    url = request.path
    print(url)
    er = ''
    if f:
        id = models.User.objects.filter(username=u)[0].id
        if request.method == 'GET':
            return render(request, 'main.html', {'er': er, 'user': u, 'url': url})
        elif request.method == "POST":
            pass

    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def datas(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        id = models.User.objects.filter(username=u)[0].id
        if request.method == 'GET':
            lists = []
            new_lists=[]
            lists.append(['%.4f' % random.uniform(0, 10) for _ in range(7)])
            lists.append(['%.4f' % random.uniform(0, 0.4) for _ in range(7)])
            lists.append(['%.4f' % random.uniform(0, 8) for _ in range(7)])
            lists.append(['%.4f' % random.uniform(0, 4) for _ in range(7)])
            lists.append(['%.4f' % random.uniform(0, 2) for _ in range(7)])
            lists.append(['%.4f' % random.uniform(0, 1) for _ in range(7)])
            lists.append(['%.4f' % random.uniform(0, 4) for _ in range(7)])
            for row in range(7):
                new_list=[]
                for t in range(7):
                    new_list.append(float(lists[row][t]))
                new_lists.append(new_list)
            result=da(new_lists)
            result=json.dumps(result)
            models.Datas.objects.create(all_data=json.dumps(lists), result=result)
            return render(request, 'datas.html', {'er': er, 'user': u, 'lists': lists, 'result': result})
        elif request.method == "POST":
            pass
            # datas=models.Datas.objects.last()
            # lists=datas.all_data
            # print(lists)
            # result=datas.result
            # print(result)
            # return render(request, 'datas.html', {'er': er, 'user': u,'lists':lists,'result':result})

    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def selector(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        lists = ''
        id = models.User.objects.filter(username=u)[0].id
        if request.method == 'GET':
            return render(request, 'select.html', {'er': er, 'user': u})
        elif request.method == "POST":
            err = ''
            date1 = request.POST.get('date1', '')
            date2 = request.POST.get('date2', '')
            if date1 and date2:
                if date1 < date2:
                    data = models.Datas.objects.filter(create_time__gte=date1, create_time__lte=date2)
                    lists = []
                    for d in data:
                        list = [json.loads(d.all_data), d.create_time, d.result]
                        lists.append(list)
                    print(lists)
                    if data:
                        pass
                    else:
                        err = '<script>alert("未查询到相关数据！！！");</script>'
                else:
                    err = '<script>alert("结束时间应该大于开始时间！！！");</script>'
            else:
                err = '<script>alert("时间格式错误或未选择，请查看并修改！！！");</script>'
            return render(request, 'select.html', {'er': er, 'user': u, 'err': err, 'lists': lists})
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def my_forms(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        if request.method == 'GET':
            return render(request, 'form.html', {'er': er, 'user': u})
        elif request.method == "POST":
            err = ''
            date1 = request.POST.get('date1', '')
            date2 = request.POST.get('date2', '')
            if date1 and date2:
                date1 = datetime.strptime(date1, '%Y-%m-%dT%H:%M')
                date2 = datetime.strptime(date2, '%Y-%m-%dT%H:%M')
                all_secends = (date2 - date1).total_seconds()
                if date1 < date2:
                    if all_secends<=86400:
                        data = models.Datas.objects.filter(create_time__gte=date1, create_time__lte=date2)
                        if data:
                            lists = []
                            hours = []
                            for d in data:
                                hours.append(datetime.strftime(d.create_time,"%Y-%m-%d %H:00:00"))
                                list = [datetime.strftime(d.create_time,"%Y-%m-%d %H:00:00"), float(json.loads(d.result)[0]),float(json.loads(d.result)[1])]
                                lists.append(list)
                            hours.sort()
                            hours = set(hours)
                            total = []
                            for j in hours:
                                co_da = []
                                data_list = {}
                                sum1 = 0
                                sum2=0
                                for l in lists:
                                    if l[0] == j:
                                        sum1 += l[1]
                                        sum2+=l[2]
                                        co_da.append(l[1])
                                avg1 = sum1 / len(co_da)
                                avg2=sum2/len(co_da)
                                data_list[str(j)] = str(avg1)+','+str(avg2)
                                total.append(data_list)
                            begin=datetime.strftime(date1,"%Y年%m月%d日 %H:%M:%S").decode('utf-8')
                            end=datetime.strftime(date2,"%Y年%m月%d日 %H:%M:%S").decode('utf-8')
                            docx(start_time=begin,end_time=end,datas=total)
                            filename = u'电能质量报表.docx'.encode('gbk')
                            response = StreamingHttpResponse(read_file('datas.docx', 512))
                            response['Content-Type'] = 'application/msword'
                            response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
                            return response
                        else:
                            err = '<script>alert("未查询到相关数据！！！");</script>'
                    else:
                        err = '<script>alert("时间差应该在一天以内！！！");</script>'
                else:
                    err = '<script>alert("结束时间应该大于开始时间！！！");</script>'
            else:
                err = '<script>alert("时间格式错误或未选择，请查看并修改！！！");</script>'
            return render(request, 'form.html', {'er': er, 'user': u, 'err': err})

    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})
