import logging
import logging.config
from json.decoder import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.accounts.models import User
from config.settings.base import DEFAULT_LOGGING

from .serializers import ReportUserSerializer, UserSerializer

logging.config.dictConfig(DEFAULT_LOGGING)
state = getattr(settings, "STATE")
BASE_URL = "http://localhost:8000/"
GOOGLE_CALLBACK_URI = BASE_URL + "accounts/google/callback/"
GITHUB_CALLBACK_URI = BASE_URL + "accounts/github/callback/"


@api_view(["POST"])
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")

    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get("code")

    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")

    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    email_req_json = email_req.json()
    email = email_req_json.get("email")

    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "google":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


@api_view(["POST"])
def github_login(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GITHUB_KEY")
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={GITHUB_CALLBACK_URI}"
    )


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def github_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GITHUB_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GITHUB_SECRET")
    code = request.GET.get("code")
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}&accept=&json&redirect_uri={GITHUB_CALLBACK_URI}&response_type=code",
        headers={"Accept": "application/json"},
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    user_req = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_json = user_req.json()
    error = user_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    print(user_json)
    email = user_json.get("email")
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 github가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "github":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 github로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)


class GithubLogin(SocialLoginView):
    adapter_class = github_view.GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client


class UpdateUsername(GenericAPIView):
    serializer_class = UserSerializer

    @permission_classes(
        IsAuthenticated,
    )
    def put(self, request, username):
        user = User.objects.get(username=username)

        serializer = UserSerializer(
            user,
            data={
                "username": request.POST["username"],
            },
        )

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Username Update"}, status=201)
        return JsonResponse({"message": "Bad request"}, status=400)


class UpdateProfileImage(GenericAPIView):
    serializer_class = UserSerializer

    @permission_classes(
        IsAuthenticated,
    )
    def put(self, request, username):
        user = User.objects.get(username=username)

        serializer = UserSerializer(
            user,
            data={
                "profile_image": request.FILES["image"],
            },
        )

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({"message": "Image Update"}, status=201)
        return JsonResponse({"message": "Bad request"}, status=400)


class Report(GenericAPIView):
    serializer_class = ReportUserSerializer

    @permission_classes(
        IsAuthenticated,
    )
    def post(self, request, username):
        user = User.objects.get(username=username)

        serializer = ReportUserSerializer(
            data={
                "user": user.id,
                "reporter": request.user.id,
                "reason": request.POST["report_reason"],
                "reported_at": timezone.now(),
            }
        )

        if serializer.is_valid():
            serializer.save()

            user.is_active = False
            user.save()

            return JsonResponse({"message": "report success"}, status=200)
        return JsonResponse({"message": "Bad request"}, status=400)
