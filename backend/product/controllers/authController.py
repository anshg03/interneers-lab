from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from product.services.authServices import AuthService
from product.utils.exceptions import AuthException

class SignupView(APIView):
    def post(self, request: Request) -> Response:
        try:
            response=AuthService.signup_user(request.data)
            return Response(response, status=status.HTTP_201_CREATED)
        except AuthException as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
class LoginView(APIView):
    def post(self,request:Request) -> Response:
        try:
            response=AuthService.login_user(request.data)
            return Response(response, status=status.HTTP_200_OK)
        except AuthException as e:
            return Response({"error":str(e)},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
class VerifyTokenView(APIView):
    def get(self,request:Request) ->Response:
        try:
            response=AuthService.verify_token(request.headers.get("Authorization"))
            return Response(response, status=status.HTTP_200_OK)
        except AuthException as e:
            return Response({"error":str(e)},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )