import firebase_admin
from firebase_admin import auth

def authorize(request):
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    print(id_token)
    
    if id_token:
        try:
            # Verify the token against the Firebase Auth API. 
            default_app = firebase_admin.initialize_app()
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token['email']
            return email
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
            print(error_message)
            raise ValueError('Only for authenticated users.')
    else:
        # no id token - need one to be here
        raise ValueError('Only for authenticated users.')