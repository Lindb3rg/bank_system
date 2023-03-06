from flask import Blueprint, render_template,flash

from flask_security import auth_required,roles_accepted,hash_password
from forms import Register_new_user,Edit_new_user
from flask import request, redirect
from model import user_datastore,User



admin_BP = Blueprint('admin_BP', __name__)





@admin_BP.route("/register_user", methods = ["GET","POST"])
@auth_required()
@roles_accepted("Admin")
def register_user_page():
    register_user = Register_new_user()
    if register_user.validate_on_submit():
        user_datastore.create_user(email=register_user.user_email.data, password=hash_password(register_user.password.data),roles=[register_user.user_role.data])
        user_datastore.db.session.commit()
        flash(f"{register_user.user_role.data} user {register_user.user_email.data} added to database")
    return render_template("admin_templates/register_user.html", register_user=register_user)






@admin_BP.route("/edit_user", methods = ["GET","POST"])
@auth_required()
@roles_accepted("Admin")
def edit_user_page():

    id = request.args.get('id')
    edit_user = Edit_new_user()
    edit_user.current_user.data = int(id)

    all_users = User.query.all()
   
    for i in all_users:
        edit_user.user_list.choices.append(i.email)
    if edit_user.validate_on_submit():
        
        user = user_datastore.find_user(email=edit_user.user_list.data)
        if edit_user.user_role.data == "Admin":
            
            role = user_datastore.find_role("Cashier")
            user.roles.remove(role)
            role = user_datastore.find_role("Admin")
            user_datastore.add_role_to_user(user,role)

            

        if edit_user.user_role.data == "Cashier":
            role = user_datastore.find_role("Admin")
            user.roles.remove(role)
            role = user_datastore.find_role("Cashier")
            user_datastore.add_role_to_user(user,role)
            

     

        if edit_user.user_email.data:
            user.email = edit_user.user_email.data
        
        if edit_user.password.data:
            user.password = hash_password(edit_user.password.data)

        
        user_datastore.db.session.commit()
        flash(f"Changes Saved!")
    return render_template("admin_templates/edit_user.html", edit_user=edit_user)




@admin_BP.route("/users")
@auth_required()
@roles_accepted("Admin")
def list_users():
    current_users = User.query.all()
    return render_template("admin_templates/users.html",current_users=current_users)





@admin_BP.route("/status/<id>", methods=["GET"])
@auth_required()
@roles_accepted("Admin")
def manage_user_status(id):
    user = user_datastore.find_user(id=id)
    status = request.args.get('status')
    
    if status == "true":
        user.active = False
        user_datastore.db.session.commit()
        
        
        return redirect("/users")
    
    if status == "false":
        user.active = True
        user_datastore.db.session.commit()
        return redirect("/users")
    
    





 