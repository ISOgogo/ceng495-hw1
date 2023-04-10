from app import (app, mongo_session, mongo_db, session, request, check_auth, check_admin)
from flask import render_template, redirect
from models.item.queries import ItemQueryOps
from models.item.base import Item
from models.review.base import Review
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
    items = mongo_transaction_with_retry(lambda: item_query_ops.search({}))
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
            result_msg = 'Price must be greater than 0!'
        except InvalidName as e:
            result_status = False
            result_msg = 'Name can not be empty!'
        except Exception as e:
            result_status = False
            result_msg = str(e)

        if result_status == True:
            return redirect('/')
        if result_status == False:
            print(result_msg)
            session['result_msg'] = result_msg
            return redirect('/create_item')

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
                mongo_transaction_with_retry(lambda: item_query_ops.delete_by_name(name))
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