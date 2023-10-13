from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import MyForm
from .models import projects
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import base64
import pickle






def home(request):
    return redirect('/proj1')

class dataMange:
    def __init__(self,data):
        expected_pred = data['expected_pred']
        pred = data['pred']
        tableData = data['rowsData']
        self.table_head = list(tableData.keys())
        self.table_head.append("Expected_Pred")
        self.table_head.append("Pred")

        self.table_items = []
        length = len(next(iter(tableData.values()))) # select first dictionary and get length of that first dict
        for i in range(length):
            list_data =[]
            for key, value in tableData.items():
                value = [math.ceil(x * 100) / 100 if isinstance(x, float) else x for x in value]
                list_data.append(value[i])
            list_data.append(expected_pred[i])
            list_data.append(pred[i])
            self.table_items.append(list_data)








# Serialize and store the object in the session
def store_object_in_session(request):
    project_instance = projects()
    serialized_data = pickle.dumps(project_instance)
    encoded_data = base64.b64encode(serialized_data).decode('utf-8')
    request.session['my_project'] = encoded_data
    return JsonResponse({'message': 'store success'})


# this id for retrive object form session
def retrieve_object_from_session(request):
    encoded_data = request.session.get('my_project')
    print(request.session.session_key)
    if encoded_data:
        decoded_data = base64.b64decode(encoded_data.encode('utf-8'))
        deserialized_project_instance = pickle.loads(decoded_data)
        return deserialized_project_instance
    return HttpResponseBadRequest('Object not found in session')

# this for jquery objstore form every project
def store_object(request,obj):
    project_instance = obj
    serialized_data = pickle.dumps(project_instance)
    encoded_data = base64.b64encode(serialized_data).decode('utf-8')
    request.session['obj'] = encoded_data
    return JsonResponse({'message': 'store success'})

# this for jquery retrive obj
def retrieve_object(request):
    encoded_data = request.session.get('obj')
    if encoded_data:
        decoded_data = base64.b64decode(encoded_data.encode('utf-8'))
        deserialized_project_instance = pickle.loads(decoded_data)
        return deserialized_project_instance
    return HttpResponseBadRequest('Object not found in session')




def proj1(request):
    store_object_in_session(request)
    obj = retrieve_object_from_session(request)
    obj.project1()
    store_object(request,obj)
    projectName = obj.project1.projectName
    data_info = obj.project1.data_info()
    test_accuracy = obj.project1.test_accuracy

    input_field = data_info['input_field']   # list of input or columns
    maped_dist = data_info['maped_dist']     #data maped to number dict
    table_manage = dataMange(test_accuracy)

    form = MyForm(input_names=input_field, maped_data=maped_dist)  # form 
    return render(request,"home.html",{'form': form,'test_accuracy':test_accuracy,'data_info':data_info,'tableMange':table_manage,'projectName':projectName})


def proj2(request):
    store_object_in_session(request)
    obj = retrieve_object_from_session(request)
    obj.project2()
    store_object(request,obj)

    projectName = obj.project2.projectName
    data_info = obj.project2.data_info()
    test_accuracy = obj.project2.test_accuracy
    input_field = data_info['input_field']
    maped_dist = data_info['maped_dist']
    tableData = test_accuracy['rowsData']

    table_manage = dataMange(test_accuracy)

    form = MyForm(input_names=input_field, maped_data=maped_dist) #form 
    return render(request,"home.html",{'form': form,'test_accuracy':test_accuracy,'data_info':data_info,'tableMange':table_manage,'projectName':projectName})



@csrf_exempt
def post_view(request):
    obj = retrieve_object(request)
    response_data = {}
    if request.method == 'POST':
        formdata = request.POST.dict()
        formdata.pop('csrfmiddlewaretoken', None)
        path = formdata.pop('path',None)
        for key, value in formdata.items():
            try:
                formdata[key] = int(value)
            except (ValueError, TypeError):
                try:
                    formdata[key] = float(value)
                except (ValueError, TypeError):
                    pass
        if path == '/proj1':
            res = obj.project1.pred_input(formdata,'processData')
            response_data = {'message': res}
        elif path == '/proj2':
            res = obj.project2.pred_input(formdata,'processData')
            response_data = {'message': res}

        return JsonResponse(response_data)

















