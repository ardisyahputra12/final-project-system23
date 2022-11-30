import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import home_bp


@home_bp.route("/banner", methods=["GET"])
def get_image():
    req = request.args
    
    # For testing only
    run_query(f"DELETE FROM categories", True)
    run_query(insert(Categories).values(id='cid1',name='baju',status='available',create_at=format_datetime(),create_by='admin'),True)
    run_query(insert(Categories).values(id='cid2',name='celana',status='available',create_at=format_datetime(),create_by='admin'),True)
    run_query(insert(Products).values(name='baju',price='200',condition='new',detail='detail',id='pid1',images_url='images_1',size='M',create_at=format_datetime(),create_by='admin',category_id='cid1'),True)
    run_query(insert(Products).values(name='baju',price='250',condition='soft',detail='detail',id='pid2',images_url='images_2',size='XL',create_at=format_datetime(),create_by='admin',category_id='cid1'),True)
    run_query(insert(Products).values(name='celana',price='150',condition='new',detail='detail',id='pid3',images_url='images_3',size='S',create_at=format_datetime(),create_by='admin',category_id='cid2'),True)
    
    query = run_query(select(Products.id,Products.images_url,Products.detail,Categories.name))
    return success_message(200, data=query)
    
@home_bp.route("/category", methods=["GET"])
def get_category():
    req = request.args
    product_categories = req.get("product_categories")
    
    # For testing only
    run_query(f"DELETE FROM categories", True)
    run_query(insert(Categories).values(id='cid1',name='baju',status='available',create_at=format_datetime(),create_by='admin'),True)
    run_query(insert(Categories).values(id='cid2',name='celana',status='available',create_at=format_datetime(),create_by='admin'),True)
    run_query(insert(Products).values(name='baju',price='200',condition='new',detail='detail',id='pid1',images_url='images_1',size='M',create_at=format_datetime(),create_by='admin',category_id='cid1'),True)
    run_query(insert(Products).values(name='baju',price='250',condition='soft',detail='detail',id='pid2',images_url='images_2',size='XL',create_at=format_datetime(),create_by='admin',category_id='cid1'),True)
    run_query(insert(Products).values(name='celana',price='150',condition='new',detail='detail',id='pid3',images_url='images_3',size='S',create_at=format_datetime(),create_by='admin',category_id='cid2'),True)
    
    if product_categories == None:
        return error_message(400, "product_categories can't empty.")
    elif product_categories != None:
        query = run_query(select(Products.id,Products.images_url,Products.detail).where(Products.name==product_categories))
        if query !=[]:
            return success_message(200, data=query)
        else:
            return error_message(400,"product not available")