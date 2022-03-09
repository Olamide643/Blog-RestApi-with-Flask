from social import db
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required
from social.model.Model import *

user = Blueprint("user",__name__)


@user.route("/register", methods = ["POST"])
def register():
    body = request.get_json()
    username = User.query.filter_by(username = body['username']).first()
    email = User.query.filter_by(email = body['email']).first()
    if username or email:
        return jsonify({"message": "username or mail already exist"})
    if body["password"] != body["confirm_password"]:
        return jsonify({"message": "password mismatch"})
    
    try:
        user = User(username = body['username'], email = body['email'], password = body["password"],
                    fullname = body['fullname'], profile_picture = body["profile_picture"],
                    bio = body["bio"])
        user.hashpassword()
        db.session.add(user)
        db.session.commit()
        return jsonify({"message" : "User successfully created"})
    except Exception as err:
        return jsonify({"message" : err})

@user.route('/login', methods = ["POST"])
def login():
    body = request.get_json()
    username = body["username"]
    password = body["password"]
    
    user = User.query.filter_by(username = username).first()
    if user and user.checkpassword(password):
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity = str(user.id), expires_delta = expires)
        return jsonify( {"tokrn": access_token})
    return {"message": "Email or Password Invalid"}
        


# This function checks if a user id following a user
# req_usr_id ---> Requesting User  ID 
# following_id ==> ID of the following ID
def is_following(req_usr_id, following_id):
    return Follow.query.filter(Follow.follower_id == req_usr_id,
                                  Follow.following_id == following_id).count() > 0

# This function check if a user id is valid  
def check_user_exist(user_id):
    query =  f''' Select * from user where id = {user_id}'''
    print(db.session.execute(query))


# This function checks if a user likes a post or not 
# req_usr_id ==> Requesting User ID
# post_id ==> ID of the post 
def has_liked_post(req_usr_id,post_id):
    return Like.query.filter(Like.post_id == post_id, 
                                Like.user_id == req_usr_id).count() > 0

#This function returns struct for a post id
# req_usr_id ==> Requesting User ID
# post_id ==> ID of the post 
def return_struct(req_usr_id,post_id):
    post = Post.query.get(post_id)
    if post:
        user = User.query.get(post.user_id)
        owner = {
            "id": user.id,
            "username" :user.username,
            "full_name": user.fullname,
            "profile_picture":user.profile_picture,
            "followed": is_following(req_usr_id, user.id)
        }
        
        post ={
            "id": post.id,
            "description": post.description,
            "owner": owner,
            "image": post.image ,
            "created_at": post.created_at,
            "liked": has_liked_post(req_usr_id, post_id)
        }  
    else:
        post = None
    return post

#This function returns the intended struct
@jwt_required
@user.route('/getsignature', methods = ["POST"])
def get_signature():
    body = request.get_json()
    req_usr_id = body["user_id"]
    post_ids = body["post_ids"]
    
    
    
    #Checks if the requesting user id is valid
    req_usr = check_user_exist(req_usr_id)
    if req_usr is None:
        return {"message": "Requesting User Id does not exist"}
    
    data = [] # Initialize an empty array for the response 
    for post_id in post_ids:
        response = return_struct(req_usr_id, post_id)
        data.append(response)
    return jsonify(data)
    




    
    

    
    

    
    
    