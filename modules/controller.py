from app import (app, mongo_session, mongo_db, session, request, check_auth, check_admin)
from flask import render_template, redirect
from models.item.queries import ItemQueryOps
from models.user.queries import UserQueryOps
from models.review.queries import ReviewQueryOps
from models.item.base import Item
from models.review.base import Review
from models.user.base import User
from modules.commons import mongo_transaction_with_retry
from modules.schema import *
from pymongo.errors import PyMongoError
from custom_errors import *
from . import controller_bp

@controller_bp.route('/', methods=['GET'])
@check_auth
def index():
    result_msg = session.pop("result_msg", "")
    item_query_ops = ItemQueryOps(mongo_db, mongo_session)
    category = request.args.get('category', None)
    if category is None or category == "All":
        items = mongo_transaction_with_retry(lambda: item_query_ops.search({}))
    else:
        items = mongo_transaction_with_retry(lambda: item_query_ops.search({"category": category}))

    return render_template('index.html', result_msg = result_msg, items=items)

@controller_bp.route('/create_item', methods=['GET','POST'])
@check_admin
def create_item():
    if request.method == 'GET':
        result_msg = session.pop("result_msg", "")
        return render_template('create_item.html', result_msg = result_msg)
    if request.method == 'POST':
        result_status = True
        result_msg = 'Item created successfully!'
        try:
            create_item_params = CreateItemParams(
                name = request.form.get('name'),
                price = request.form.get('price'),
                description = request.form.get('description'),
                seller = request.form.get('seller'),
                image = request.form.get('image'),
                size = request.form.get('size'),
                colour = request.form.get('colour'),
                spec = request.form.get('spec'),
                category= request.form.get('category')
                )
            new_item = Item(
                name = create_item_params.name,
                price = create_item_params.price,
                description = create_item_params.description,
                seller = create_item_params.seller,
                image = create_item_params.image,
                size = create_item_params.size,
                colour = create_item_params.colour,
                spec = create_item_params.spec,
                category= create_item_params.category
            )

            item_query_ops = ItemQueryOps(mongo_db, mongo_session)
            mongo_transaction_with_retry(lambda: item_query_ops.create(new_item))
        except PyMongoError as e:
            result_status = False
            result_msg = 'Database connection error. Please try again later!'
        except InvalidPrice as e:
            result_status = False
            result_msg = 'Price must be greater than 0 and correct form Ex:(9.99)'
        except InvalidName as e:
            result_status = False
            result_msg = 'Name can not be empty!'
        except InvalidUrl as e:
            result_status = False
            result_msg = 'Image url is not valid!'
        except Exception as e:
            result_status = False
            result_msg = str(e)

        if result_status == True:
            return redirect('/')
        if result_status == False:
            session['result_msg'] = result_msg
            return redirect('/create_item')

@controller_bp.route('/item/<item>/review', methods=['GET','POST'])
@check_auth
def review(item):
    item_query_ops = ItemQueryOps(mongo_db, mongo_session)
    review_query_ops = ReviewQueryOps(mongo_db, mongo_session)
    reviews = mongo_transaction_with_retry(lambda: review_query_ops.search({'item': item}))
    user_old_review = mongo_transaction_with_retry(lambda: review_query_ops.find_one(session["username"], item))

    if request.method == 'GET':
        result_msg = session.pop("result_msg", "")
        item = mongo_transaction_with_retry(lambda: item_query_ops.get_by_name(item))
        return render_template('reviews.html', item=item, result_msg = result_msg, reviews = reviews, user_old_review=user_old_review)
    
    if request.method == 'POST':
        result_status = True
        result_msg = 'Review Added successfully!'
        user_query_ops = UserQueryOps(mongo_db, mongo_session)
        try:
            if user_old_review:
                user_old_review.rating = request.form.get('rating')
                user_old_review.review = request.form.get('review')
                mongo_transaction_with_retry(lambda: review_query_ops.update(user_old_review))
            else:
                new_review = Review(user=session['username'], 
                                    item=item, 
                                    rating=request.form.get('rating'), 
                                    review=request.form.get('review')
                                    )
                mongo_transaction_with_retry(lambda: review_query_ops.create(new_review))
            # Update avg rating for item and the user
            mongo_transaction_with_retry(lambda: item_query_ops.update_avg_rating(item_name = item, 
                                                                                    review_query_ops = review_query_ops))
            mongo_transaction_with_retry(lambda: user_query_ops.update_avg_rating(user_name = session['username'], 
                                                                                    review_query_ops = review_query_ops))

        except PyMongoError as e:
            result_status = False
            result_msg = 'Database connection error. Please try again later!'
        except LongTextError as e:
            result_status = False
            result_msg = 'Review can not be longer than 140 charachter!'
        except RangeError as e:
            result_status = False
            result_msg = 'Rating must be in range [1-5]'
        except Exception as e:
            result_status = False
            result_msg = str(e)
          
        if result_status == False: 
            session['result_msg'] = result_msg

        return redirect('/item/'+item+'/review')

@controller_bp.route('/item/<name>', methods=['GET','POST'])
@check_auth
def item(name):
    if request.method == 'GET':
        result_msg = session.pop("result_msg", "")
        item_query_ops = ItemQueryOps(mongo_db, mongo_session)
        item = mongo_transaction_with_retry(lambda: item_query_ops.get_by_name(name))
        return render_template('item.html', item=item, result_msg = result_msg)

    if request.method == 'POST':
        result_status = True
        result_msg = 'Item updated successfully!'
        try:    
            if request.args.get('delete') == 'true':
                item_query_ops = ItemQueryOps(mongo_db, mongo_session)
                review_query_ops = ReviewQueryOps(mongo_db, mongo_session)
                user_query_ops = UserQueryOps(mongo_db, mongo_session)
                mongo_transaction_with_retry(lambda: item_query_ops.delete_by_name(name))
                mongo_transaction_with_retry(lambda: review_query_ops.delete_item_reviews(name, user_query_ops))
                return redirect('/')

            create_item_params = CreateItemParams(
                name = request.form.get('name'),
                price = request.form.get('price'),
                description = request.form.get('description'),
                seller = request.form.get('seller'),
                image = request.form.get('image'),
                size = request.form.get('size'),
                colour = request.form.get('colour'),
                spec = request.form.get('spec'),
                category= request.form.get('category')
            )
            item_query_ops = ItemQueryOps(mongo_db, mongo_session)
            mongo_transaction_with_retry(lambda: item_query_ops.update_with_params(create_item_params))
            
        except PyMongoError as e:
            result_status = False
            result_msg = 'Database connection error. Please try again later!'
        except InvalidPrice as e:
            result_status = False
            result_msg = 'Price must be greater than 0!'
        except InvalidName as e:
            result_status = False
            result_msg = 'Name can not be empty!'
        except Exception as e:
            result_status = False
            result_msg = str(e)
        
        if result_status == True:
            return redirect('/item/' + name)
        if result_status == False:
            session['result_msg'] = result_msg
            return redirect('/item/' + name)

@controller_bp.route('/users/delete/<username>', methods=['POST'])
@check_admin
def users_delete(username): 
    result_status = True
    result_msg = 'User Deleted Successfully'
    try:
        user_query_ops = UserQueryOps(mongo_db, mongo_session)
        review_query_ops = ReviewQueryOps(mongo_db, mongo_session)
        item_query_ops = ItemQueryOps(mongo_db, mongo_session)
        
        mongo_transaction_with_retry(lambda: user_query_ops.delete_by_username(username))
        mongo_transaction_with_retry(lambda: review_query_ops.delete_user_reviews(username, item_query_ops))

    except PyMongoError as e:
        result_status = False
        result_msg = 'Database connection error. Please try again later!'
    except Exception as e:
        result_status = False
        result_msg = str(e)

    if result_status == False:
        session['result_msg'] = result_msg

    return redirect('/users')

@controller_bp.route('/users/create', methods=['POST'])
@check_admin
def users_create():
    result_status = True
    result_msg = 'User Created Successfully'
    try:
        new_user = User(email=request.form.get("email"), 
                        username=request.form.get("username"), 
                        password=request.form.get("password")
                        )

        user_query_ops = UserQueryOps(mongo_db, mongo_session)
        mongo_transaction_with_retry(lambda: user_query_ops.create(new_user))
    except PyMongoError as e:
        result_status = False
        result_msg = 'Database connection error. Please try again later!'
    except Exception as e:
        result_status = False
        result_msg = str(e)

    if result_status == False:
        session['result_msg'] = result_msg

    return redirect('/users')

@controller_bp.route('/users', methods=['GET'])
@check_admin
def users_view():
    result_msg = session.pop("result_msg", "")
    user_query_ops = UserQueryOps(mongo_db, mongo_session)
    users = mongo_transaction_with_retry(lambda: user_query_ops.search({}))
    return render_template('users.html', result_msg = result_msg, users = users)