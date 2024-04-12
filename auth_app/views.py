from datetime import datetime
from django.shortcuts import render
from Src_App.views import * 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


def set_password(request):

    if request.method == 'POST':
        password = request.POST.get('password')
        current_user = request.user 

        if current_user:
            current_user_profile = UserProfile.objects.get(user=current_user)
            current_user_profile.setting_access_code =  password
            current_user_profile.save()
            
    return redirect('settings')


# @api_view(['GET','POST'])
# @csrf_exempt
# def thrive_cart_webhook(request):

#     if request.method == 'POST':
#         print("There is something happening to me.")
#         try:
#             payload = json.loads(request.body)

#             if payload['event'] == 'order.success':
#                 customer_email = payload.get('customer').get('email')

#                 user = User.objects.get(email=customer_email)
#                 # print(user)
#                 if user:
#                     user_profile = UserProfile.objects.get(user=user)
#                     # print(user_profile)
#                     if user_profile:
#                         user_profile.has_subscription = True 
#                         user_profile.subscribed_on = datetime.now()
#                         user_profile.save()

#                         # print('Everything Okay.')
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#             return Response({'mes':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return Response({"mes": "Got it"}, status=status.HTTP_200_OK)


@csrf_exempt
def thrive_cart_webhook(request):
    message = None
    if request.method == 'POST' or request.method == 'HEAD':
        try:
            payload = json.loads(request.body)
            base_product_name = payload.get('base_product_name')
            if payload['event'] == 'order.success':
                customer_email = payload.get('customer').get('email')
                user = User.objects.get(email=customer_email)
                if user:
                    user_profile = UserProfile.objects.get(user=user)
                    if base_product_name == 'TaterTot Kids Club Membership':
                        if user_profile:
                            user_profile.has_subscription = True 
                            user_profile.subscribed_on = datetime.now()
                            user_profile.save()
                            return JsonResponse({"mes": "Successfully Got it"}, status=200)
                    elif base_product_name == 'Music App Subscription':
                        if user_profile:
                            user_profile.has_music_subscription = True
                            user_profile.music_subscribed_on = datetime.now()
                            user_profile.save() 
                            return JsonResponse({"mes": "Successfully Got it"}, status=200)
        except Exception as e: 
            message = "An error occured"
    return JsonResponse({"mes": message }, status=200)




def subscription(request):
    
    return render(request, 'thrivecartCheckout.html')


def admin_login(request):

    message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, username=email, password=password)

            if user and user.is_superuser:
                login(request, user)
                return redirect('admin-home')
            elif user and not user.is_superuser:
                message = "You have an account but are not allowed to access Admin Panel"
            elif not user:
                message = "Invalid Credentials"

    return render(request, 'admin_panel_templates/login.html', {'message':message})


def times_up(request):

    context = {}
    return render(request, 'timesUp.html', context)


def music_subscription(request):

    return render(request, 'musicAppTemplates/music_subscription.html')


def change_password(request):
    message = None
    response_status = None 
    try:
        request_body = json.loads(request.body) 
        user = request.user
        user = User.objects.get(id=int(user.id))
        new_password = request_body.get('password')
        response_status = 200
        if new_password is not None:
            user.password = new_password 
            user.save()
    except Exception as e:
        print(e)
        message = e
        response_status = 500

    return JsonResponse({'message':message}, status=response_status)