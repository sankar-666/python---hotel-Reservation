from flask import *
from database import *

user=Blueprint('user',__name__)

@user.route('/userhome')
def userhome():
    q="select * from user where login_id='%s'"%(session['loginid'])
    res=select(q)
    print(res)
    name=res[0]['fname']+"\t"+res[0]['lname']
    print(name)
    return render_template('userhome.html',name=name)

@user.route('/view_food')
def view_food():
    data={}
    q="select * from food"
    data['res']=select(q)
    return render_template('view_food.html',data=data)




@user.route('/add_to_cart',methods=['get','post'])
def add_to_cart():
    data={}
    iid=request.args['iid']
    cp=request.args['cp']
    # mu=request.args['mu']
    item=request.args['item']


    if 'btn' in request.form:
        total = request.form['total']
        rstock = request.form['rstock']

        q="select * from ordermaster where order_status='pending' and user_id='%s'"%(session['uid'])
        res=select(q)
        if res:
            oid=res[0]['ordermaster_id']
        else:
            q="insert into ordermaster values(null,'%s',0,curdate(),'pending')"%(session['uid'])
            oid=insert(q)
        q="select * from orderdetails where food_id='%s' and ordermaster_id='%s'"%(iid,oid)
        val=select(q)
        if val:
            q="update orderdetails set quantity=quantity+'%s', total_amount=total_amount+'%s' where food_id='%s' and ordermaster_id='%s' "%(rstock,total,iid,oid)
            update(q)
        else:
            q="insert into orderdetails values (null,'%s','%s','%s','%s','pending')"%(oid,iid,rstock,total)
            insert(q)
        q="update ordermaster set totalamount=totalamount+'%s' where ordermaster_id='%s'"%(total,oid)
        update(q)
        flash("Successfully added to Cart")
        return redirect(url_for("user.view_food"))

   
    return render_template('add_to_cart.html',data=data,item=item,cp=cp)




@user.route('/cart')
def cart():
    data={}
    q="SELECT * FROM `ordermaster`,`orderdetails`,`food` WHERE `ordermaster`.`ordermaster_id`=`orderdetails`.`ordermaster_id` AND `orderdetails`.`food_id`=`food`.`food_id` AND `ordermaster`.`user_id`='%s' and order_status='pending'"%(session['uid'])
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        ccid=request.args['ccid']
        cmid=request.args['cmid']
        price=request.args['price']
    else:
        action = None

    if action =="remove":
        q="delete from orderdetails where cc_id='%s'"%(ccid)
        delete(q)
        q="update ordermaster set totalamount=totalamount-'%s' where ordermaster_id='%s'"%(price,cmid)
        update(q)
        q="select * from orderdetails where ordermaster_id='%s'"%(cmid)
        val=select(q)
        if val:
            print("hameeeee")
        else:
            q="delete from ordermaster where ordermaster_id='%s'"%(cmid)
            delete(q)
        return redirect(url_for("customer.cart"))

    return render_template('cart.html',data=data)



@user.route('/customer_make_payment',methods=['get','post'])
def customer_make_payment():
    data={}
    omid=request.args['omid']
    amount=request.args['amount']
    if 'btn' in request.form:
        q="insert into payment values (null,'%s','food','%s',curdate())"%(omid,amount)
        insert(q)
        q="update ordermaster set order_status='payment completed'  where ordermaster_id='%s'"%(omid)
        update(q)
        flash("Payment Completed")
        return redirect(url_for("user.userhome"))
    return render_template('customer_make_payment.html',data=data,total=amount)

@user.route('/user_room_payment',methods=['get','post'])
def user_room_payment():
    data={}
    omid=request.args['omid']
    amount=request.args['amount']
    if 'btn' in request.form:
        q="insert into payment values (null,'%s','room','%s',curdate())"%(omid,amount)
        insert(q)
        q="update booking set status='payment completed'  where booking_id='%s'"%(omid)
        update(q)
        flash("Payment Completed")
        return redirect(url_for("user.userhome"))
    return render_template('user_room_payment.html',data=data,total=amount)



@user.route('/food_bookings')
def food_bookings():
    data={}
    q="SELECT * FROM `ordermaster`,`orderdetails`,`food` WHERE `ordermaster`.`ordermaster_id`=`orderdetails`.`ordermaster_id` AND `orderdetails`.`food_id`=`food`.`food_id` AND `ordermaster`.`user_id`='%s' and order_status <> 'pending'"%(session['uid'])
    data['res']=select(q)
    return render_template("food_bookings.html",data=data)


@user.route('/user_room_bookings')
def user_room_bookings():
    data={}
    q="SELECT * FROM `booking`,`room` WHERE `booking`.`room_id`=`room`.`room_id` AND `booking`.`user_id`='%s'"%(session['uid'])
    data['res']=select(q)
    return render_template("user_room_bookings.html",data=data)


@user.route('/view_rooms')
def view_rooms():
    data={}
    q="SELECT * FROM room"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        rid=request.args['rid']
        rate=request.args['rate']
    else:
        action=None

    if action == "book":
        q="select * from booking where room_id='%s' and user_id='%s'"%(rid,session['uid'])
        res=select(q)
        if res:
            flash("you Have Alrady booked this room")
        else:
            q="insert into booking values (null,'%s','%s','%s',curdate(),'pending')"%(session['uid'],rid,rate)
            insert(q)
            flash("Room Booked")
            return redirect(url_for("user.userhome"))

    return render_template("view_rooms.html",data=data)


@user.route("/customer_send_complaint",methods=['get','post'])
def customer_send_complaint():
    data={}

    cid=session['uid']

    if 'btn' in request.form:
        comp=request.form['comp']

        q="insert into complaint values(NULL,'%s','%s','pending',curdate())"%(cid,comp)
        print(q)
        insert(q)
        return redirect(url_for("user.customer_send_complaint"))
    
    q="select * from complaint where user_id='%s'"%(cid)
    data['res']=select(q)
    return render_template("customer_send_complaint.html",data=data)