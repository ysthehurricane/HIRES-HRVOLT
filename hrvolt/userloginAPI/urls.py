from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('registerUser', views.UserRegisterAPI.as_view(), name="registerPage"),
    path('loggedInUpdateUser', views.UserloggedInUpdateAPI.as_view(), name="loggedInUpdateUserPage"),

    path('UserRegisterdemo', views.UserRegisterdemoAPI.as_view(), name="UserRegisterdemoPage"),

    path('UserIdGet', views.UserIdGetAPI.as_view(), name="UserIdGetPage"),

    path('generateToken/', TokenObtainPairView.as_view(), name='tokenObtainPair'),
    path('refreshToken/', TokenRefreshView.as_view(), name='tokenRefresh'),
    path('verifyToken/', TokenVerifyView.as_view(), name='tokenVerify'),

    path('emailVerificationUser', views.EmailVerificationAPI.as_view(), name="emailVerficationPage"),
    path('emailVerificationCompletion', views.EmailVerificationCompletionAPI.as_view(), name="emailVerficationCompletionPage"),

    path('loginUser', views.UserLoginAPI.as_view(), name="loginPage"),
    path('logoutUser', views.UserLogoutAPI.as_view(), name="logoutPage"),

    path('forgetPasswordUser', views.UserForgetPasswordAPI.as_view(), name="ForgetPasswordPage"),
    path('forgetPasswordUserChanged', views.ForgotPasswordChangedAPI.as_view(), name="ForgetPasswordChangedPage"),
    path('changePasswordUser', views.UserChangePasswordAPI.as_view(), name = "ChangePasswordPage"),

    # path('UserEditProfile', views.UserEditProfileAPI.as_view(), name = "UserEditProfilePage"),

    path('UserEditProfile', views.UserEditProfileAPI.as_view(), name = "UserEditProfilePage"),

    path('ViewUserProfile', views.ViewUserProfileAPI.as_view(), name = "ViewUserProfilePage"),

    path('getuserdata',views.GetUserdataAPI.as_view(),name="UserGetDataPage"),

    path('UserContractRegister',views.UserContractRegisterAPI.as_view(),name="UserContractRegisterPage"),
    path('UserContractGet',views.UserContractGetAPI.as_view(),name="UserContractGetPage"),

    # path('DeleteLoggedUser',views.DeleteLoggedUserAPI.as_view(),name="DeleteLoggedUserPage"),

]