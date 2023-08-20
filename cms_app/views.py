import json
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
import io
from rest_framework.parsers import JSONParser
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db.models import Q

#TODO Main Started

@csrf_exempt
def cms_api_data(request):
    param_main = request.GET.get('type')
    #TODO - GET Method -------------------------------------------------------------------------------------------------
    if request.method == 'GET':
        # TODO - PARAM Checking ----------------------------------------------------------------------------------------
        if param_main.lower() == 'user':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('user_id', None)
            if id is not None:
                stu = info_user.objects.get(user_id=id)
                serializer = info_usersSerializer(stu)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data,content_type='application/json')
            stu = info_user.objects.all()
            serializer = info_usersSerializer(stu,many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        elif param_main.lower() == 'blog':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            u_id = pythondata.get('user_id', None)

            if u_id:
                stu = post_blog.objects.filter(user_id=u_id)
                serializer = BlogSerializer(stu, many=True)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
            else:
                search_query = pythondata.get('search_query', None)
                if search_query is not None:
                    stu = post_blog.objects.filter(Q(title__icontains = search_query) | Q(description__icontains = search_query) | Q(content__icontains = search_query), post_type='public')
                    serializer = BlogSerializer(stu, many=True)
                    json_data = JSONRenderer().render(serializer.data)
                    loaded_json = json.loads(json_data)
                    post_dict = {}
                    for i in loaded_json:
                        post_id_main = i['post_id']
                        post_dict[f"Post {post_id_main}"] = i
                        try:
                            likes_main = like_data.objects.get(post_id = post_id_main).likes
                        except:
                            likes_main = 0
                        post_dict[f'Post {post_id_main} likes'] = likes_main

                    return JsonResponse(post_dict, safe=False)

                stu = post_blog.objects.filter(post_type = 'public')
                serializer = BlogSerializer(stu, many=True)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
        else:
            return JsonResponse({"Message": f"Type {param_main} is not Valid"})

    #TODO - POST Method -------------------------------------------------------------------------------------------------
    if request.method == 'POST':
        # TODO - PARAM Checking ----------------------------------------------------------------------------------------
        if param_main.lower() == 'user':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            serializer = info_usersSerializer(data=pythondata)
            if serializer.is_valid():
                serializer.save()
                res = {'msg': 'User Create Sucessfull.....'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
        elif param_main.lower() == 'blog':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            req_user_id = pythondata.get('user_id', None)
            try:
                user_id_def = info_user.objects.get(user_id=req_user_id)
                print(user_id_def.user_id)
                stream = io.BytesIO(json_data)
                pythondata = JSONParser().parse(stream)
                serializer = BlogSerializer(data=pythondata)
                if serializer.is_valid():
                    serializer.save()
                    res = {'msg': 'Blog has been Create Successful.....'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                json_data = JSONRenderer().render(serializer.errors)
                return HttpResponse(json_data, content_type='application/json')
            except Exception as e:
                return JsonResponse({"Error": f"Requested User {req_user_id} is not Authenticated"})

        else:
            return JsonResponse({"Message": f"Type {param_main} is not Valid"})

    # TODO - PUT Method -------------------------------------------------------------------------------------------------
    if request.method == 'PUT':
        # TODO - PARAM Checking ----------------------------------------------------------------------------------------
        if param_main.lower() == 'user':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('user_id', None)
            stu = info_user.objects.get(user_id=id)
            serializer = info_usersSerializer(stu,data=pythondata,partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {'msg': 'User Details Update Sucessfull.....'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
        elif param_main.lower() == 'blog':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('post_id', None)
            stu = post_blog.objects.get(post_id=id)

            # Update the update_date field
            stu.update_date = datetime.now()  # Set to current date and time
            stu.save()  # Save the updated object

            serializer = BlogSerializer(stu,data=pythondata,partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {'msg': 'Blog Details Update Sucessfull.....'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
        else:
            return JsonResponse({"Message": f"Type {param_main} is not Valid"})

    # TODO - DELETE Method -------------------------------------------------------------------------------------------------
    if request.method == 'DELETE':
        # TODO - PARAM Checking ----------------------------------------------------------------------------------------
        if param_main.lower() == 'user':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('user_id')
            stu = info_user.objects.get(user_id=id)
            stu.delete()
            res = {'msg': 'User Delete Sucessfull.....'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        elif param_main.lower() == 'blog':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('post_id')
            stu = post_blog.objects.get(post_id=id)
            stu.delete()
            res = {'msg': 'Blog Delete Sucessfull.....'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        else:
            return JsonResponse({"Message": f"Type {param_main} is not Valid"})


