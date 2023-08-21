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


#TODO - Main started
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
            name = pythondata.get('name', None)
            if id is not None:
                stu = info_user.objects.get(user_id=id)
                serializer = info_usersSerializer(stu)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data,content_type='application/json')
            elif name is not None:
                stu = info_user.objects.get(name=name)
                serializer = info_usersSerializer(stu)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
            if pythondata == {}:
                stu = info_user.objects.all()
                serializer = info_usersSerializer(stu,many=True)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
            else:
                return JsonResponse({"Message": f"Please Choose Based On User ID or Name"})
        elif param_main.lower() == 'blog':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            u_id = pythondata.get('user_id', None)
            p_id = pythondata.get('post_id', None)

            if u_id:
                stu = post_blog.objects.filter(user_id=u_id)
                serializer = BlogSerializer(stu, many=True)
                json_data = JSONRenderer().render(serializer.data)
                loaded_json = json.loads(json_data)
                if loaded_json != []:
                    post_dict = {}
                    for i in loaded_json:
                        post_id_main = i['post_id']
                        post_dict[f"Post {post_id_main}"] = i
                        try:
                            likes_main = like_data.objects.get(post_id=post_id_main).likes
                            dislikes_main = like_data.objects.get(post_id=post_id_main).dislikes
                        except:
                            likes_main = 0
                            dislikes_main = 0
                        post_dict[f'Post {post_id_main} likes'] = likes_main
                        post_dict[f'Post {post_id_main} dislikes'] = dislikes_main
                    return JsonResponse(post_dict, safe=False)
                else:
                    return JsonResponse({"Message": f"User ID {u_id} is Still Not Post Any Blog..."})
            elif p_id:
                stu = post_blog.objects.filter(post_id=p_id,post_type='public')
                serializer = BlogSerializer(stu, many=True)
                json_data = JSONRenderer().render(serializer.data)
                loaded_json = json.loads(json_data)
                if loaded_json != []:
                    post_dict = {}
                    for i in loaded_json:
                        post_id_main = i['post_id']
                        post_dict[f"Post {post_id_main}"] = i
                        try:
                            likes_main = like_data.objects.get(post_id=post_id_main).likes
                            dislikes_main = like_data.objects.get(post_id=post_id_main).dislikes
                        except:
                            likes_main = 0
                            dislikes_main = 0
                        post_dict[f'Post {post_id_main} likes'] = likes_main
                        post_dict[f'Post {post_id_main} dislikes'] = dislikes_main
                    return JsonResponse(post_dict, safe=False)
                else:
                    stu = post_blog.objects.filter(post_id=p_id, post_type='private')
                    serializer = BlogSerializer(stu, many=True)
                    json_data = JSONRenderer().render(serializer.data)
                    loaded_json = json.loads(json_data)
                    if loaded_json != []:
                        return JsonResponse({"Message": f"This is Private Blog, To access this Blog Provide User ID. Thank You.... "})
                    else:
                        return JsonResponse({"Message": f"There is Post ID {p_id} is Not Available Kindly Choose Valid Post ID..."})
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
                            dislikes_main = like_data.objects.get(post_id = post_id_main).dislikes
                        except:
                            likes_main = 0
                            dislikes_main = 0
                        post_dict[f'Post {post_id_main} likes'] = likes_main
                        post_dict[f'Post {post_id_main} dislikes'] = dislikes_main
                    return JsonResponse(post_dict, safe=False)
                stu = post_blog.objects.filter(post_type = 'public')
                serializer = BlogSerializer(stu, many=True)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
        elif param_main.lower() == 'like':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            u_id = pythondata.get('user_id', None)
            p_id = pythondata.get('post_id', None)
            if u_id is not None:
                try:
                    stu = like_data.objects.get(user_id=u_id)
                    serializer = LikesSerializer(stu)
                    json_data = JSONRenderer().render(serializer.data)
                    return HttpResponse(json_data,content_type='application/json')
                except Exception as e:
                    return JsonResponse({"Message": f"User ID {u_id} Blog have No any Likes.. "})
            elif p_id is not None:
                try:
                    stu = like_data.objects.get(post_id=p_id)
                    serializer = LikesSerializer(stu)
                    json_data = JSONRenderer().render(serializer.data)
                    return HttpResponse(json_data,content_type='application/json')
                except Exception as e:
                    return JsonResponse({"Message": f"Post ID {p_id} Blog have No any Likes.. "})
            if pythondata == {}:
                stu = like_data.objects.all()
                serializer = LikesSerializer(stu,many=True)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
            else:
                return JsonResponse({"Message": f"Please choose User ID or Post ID for view Specific Likes"})
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
                res = {'Message': 'User Create Sucessfull.....'}
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
                    res = {'Message': 'Blog has been Create Successful.....'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                json_data = JSONRenderer().render(serializer.errors)
                return HttpResponse(json_data, content_type='application/json')
            except Exception as e:
                return JsonResponse({"Error": f"Requested User {req_user_id} is not Authenticated"})
        elif param_main.lower() == 'like':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            req_post_id = pythondata.get('post_id', None)
            if req_post_id is not None:
                try:
                    post_id_def = like_data.objects.get(post_id=req_post_id)
                    print(post_id_def.post_id)
                    print("Like on Exiting Blog....")
                    post_id_def.likes += 1
                    post_id_def.save()
                    stu = like_data.objects.get(post_id=req_post_id)
                    serializer = LikesSerializer(stu)
                    json_data = JSONRenderer().render(serializer.data)
                    return HttpResponse(json_data, content_type='application/json')
                except Exception as e:
                    try:
                        post_id_def = post_blog.objects.get(post_id=req_post_id)
                        print(post_id_def.user_id)
                        stream = io.BytesIO(json_data)
                        pythondata = JSONParser().parse(stream)
                        pythondata['user_id'] = post_id_def.user_id
                        pythondata['likes'] = 1
                        serializer = LikesSerializer(data=pythondata)
                        if serializer.is_valid():
                            serializer.save()
                            res = {'Message': 'First Like on Blog.....'}
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type='application/json')
                        json_data = JSONRenderer().render(serializer.errors)
                        return HttpResponse(json_data, content_type='application/json')
                    except Exception as e:
                        print(e)
                        return JsonResponse({"Error": f"Requested User {req_post_id} is not Authenticated"})
            else:
                return JsonResponse({"Message": f"Please choose Valid Post ID........"})
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
            try:
                stu = info_user.objects.get(user_id=id)
                serializer = info_usersSerializer(stu,data=pythondata,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    res = {'Message': 'User Details Update Sucessfull.....'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                json_data = JSONRenderer().render(serializer.errors)
                return HttpResponse(json_data, content_type='application/json')
            except Exception as e:
                return JsonResponse({"Message": f"Enter User ID {id} is not Valid User ID......"})
        elif param_main.lower() == 'blog':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('post_id', None)
            try:
                stu = post_blog.objects.get(post_id=id)
                # Update the update_date field
                stu.update_date = datetime.now()  # Set to current date and time
                stu.save()  # Save the updated object
                serializer = BlogSerializer(stu,data=pythondata,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    res = {'Message': 'Blog Details Update Sucessfull.....'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            except Exception as e:
                print(e)
                return JsonResponse({"Message": f"Sorry No any Post Available on Given Post ID {id}, Please Enter Valid Post ID."})

            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')

        elif param_main.lower() == 'dislike':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            req_post_id = pythondata.get('post_id', None)
            if req_post_id is not None:
                try:
                    post_id_def = like_data.objects.get(post_id=req_post_id)
                    print(post_id_def.post_id)
                    print("Dislike the Blog.....")
                    post_id_def.dislikes +=1
                    post_id_def.save()
                    return JsonResponse({"Message": f"Dislike the Blog....."})
                except Exception as e:
                    print(e)
                    try:
                        post_id_def = post_blog.objects.get(post_id=req_post_id)
                        print(post_id_def.user_id)
                        stream = io.BytesIO(json_data)
                        pythondata = JSONParser().parse(stream)
                        pythondata['user_id'] = post_id_def.user_id
                        pythondata['dislikes'] = 1
                        pythondata['likes'] = 0
                        serializer = LikesSerializer(data=pythondata)
                        if serializer.is_valid():
                            serializer.save()
                            res = {'Message': 'Dislike the Blog.....'}
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type='application/json')
                        json_data = JSONRenderer().render(serializer.errors)
                        return HttpResponse(json_data, content_type='application/json')
                    except Exception as e:
                        print(e)
                        return JsonResponse({"Error": f"Requested User {req_post_id} is not Authenticated"})
            else:
                return JsonResponse({"Message": f"Please choose Valod Post ID......"})
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
            if id is not None:
                try:
                    stu = info_user.objects.get(user_id=id)
                    stu.delete()
                    res = {'Message': 'User Delete Sucessfull.....'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                except Exception as e:
                    return JsonResponse({"Message": f"Please Choose Valid User ID..."})
            else:
                return JsonResponse({"Message": f"Please Choose User ID..."})
        elif param_main.lower() == 'blog':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('post_id')
            if id is not None:
                try:
                    stu = post_blog.objects.get(post_id=id)
                    stu.delete()
                    res = {'Message': 'Blog Delete Sucessfull.....'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                except Exception as e:
                    return JsonResponse({"Message": f"Please Choose Valid Post ID..."})
            else:
                return JsonResponse({"Message": f"Please Choose Post ID..."})
        elif param_main.lower() == 'like':
            json_data = request.body
            stream = io.BytesIO(json_data)
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('like_id')
            if id is not None:
                try:
                    stu = like_data.objects.get(like_id=id)
                    stu.delete()
                    res = {'Message': 'Blog Like Details Delete Sucessfull.....'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                except Exception as e:
                    return JsonResponse({"Message": f"Please Choose Valid Like ID..."})
            else:
                return JsonResponse({"Message": f"Please Choose Like ID..."})
        else:
            return JsonResponse({"Message": f"Type {param_main} is not Valid"})


