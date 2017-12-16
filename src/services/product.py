# coding=utf-8

from flask import Blueprint
from flask import jsonify
from flask import request

from models import Product


service = Blueprint('product', __name__, url_prefix='/product')


_resource_dir = ''
baseurl = 'http://104.199.172.165:8000/'


def set_resource_dir(resource_dir):
    global _resource_dir
    _resource_dir = resource_dir


@service.route('/all_raw')
def get_all_raw():
    product_model = Product()
    products = product_model.get_all()
    return jsonify({'products': products})


@service.route('/all')
def get_all():
    product_model = Product()
    products = product_model.get_all()
    products = [_create_response_product(product) for product in products]
    return jsonify({'products': products})


@service.route('/<product_id>/raw')
def get_product_raw(product_id):
    product_model = Product()
    product = product_model.find(product_id)
    return jsonify({'product': product})


@service.route('/<product_id>')
def get_product(product_id):
    product_model = Product()
    product = product_model.find(product_id)
    product = _create_response_product(product)
    return jsonify({'product': product})


@service.route('/<product_id>/image')
def get_image(product_id=''):
    try:
        product_model = Product()
        product = product_model.find(product_id)

        image = product['imgUrl']
        return jsonify({'image': image})
    except:
        return jsonify({'image': None})


@service.route('/<product_id>/image_urls')
def get_images(product_id=''):
    product_model = Product()
    product = product_model.find(product_id)
    images = [product['imgUrl']]
    colors = product['fullSaleInfo']['colors']
    for color in colors:
        images += [image for key, image in color.items()]

    return jsonify({'imageUrls': images})


@service.route('/<product_id>/contact')
def get_contact(product_id=''):
    product_model = Product()
    product = product_model.find(product_id)
    contact = product['fullSaleInfo']['call'] if product is not None else []
    return jsonify({'contact': contact})


@service.route('/<product_id>/comments')
def get_comments(product_id=''):
    product_model = Product()
    product = product_model.find(product_id)
    comments = product['fullSaleInfo']['listCmts'] if product is not None else []
    comments = [{'cmt': c['cmt'], 'date': c['date'], 'name': c['name']} for c in comments]
    return jsonify({'comments': comments})


@service.route('/<product_id>/description')
def get_description(product_id=''):
    product_model = Product()
    product = product_model.find(product_id)
    return jsonify({'description': _generate_description(product)})


def _generate_description(product):
    if product is None:
        return ''
    description = ''

    if product['category'].lower() == 'phu-kien'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'sac-dtdd'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'cap-dien-thoai'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'the-nho-dien-thoai'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'tai-nghe'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'usb'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'chuot-may-tinh'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'loa-laptop'.strip().lower():
        description = 'Loa vi tính {}'.format(product['name'])

    if product['category'].lower() == 'phu-kien-chinh-hang'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'phu-kien-khac'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'op-lung-dien-thoai'.strip().lower():
        description = product['name']

    if product['category'].lower() == 'Điện thoại'.strip().lower():
        description = 'Điện thoại {}'.format(product['name'])
        bginfo = product.get('bginfo')
        if type(bginfo) is dict:
            camera = bginfo.get('Camera')
            screen = bginfo.get('Màn hình')
            memory = bginfo.get('RAM')
            cpu = bginfo.get('CPU')
            if type(camera) is str:
                description += ' với camera {}'.format(camera)
            if type(screen) is str:
                description += ', màn hình {}'.format(screen)
            if type(memory) is str:
                description += ', bộ nhớ {}'.format(memory)
            if type(cpu) is str:
                description += ', vi xử lý {}'.format(cpu)
            price = product.get('price')
            if type(price) is str:
                description += '. Giá bán {}'.format(price)

    if product['category'].lower() == 'Laptop'.strip().lower():
        description = 'Laptop {}'.format(product['name'])
        bginfo = product.get('bginfo')
        if type(bginfo) is dict:
            cpu = bginfo.get('CPU')
            screen = bginfo.get('Màn hình')
            memory = bginfo.get('RAM')
            card = bginfo.get('Đồ họa')
            if type(cpu) is str:
                description += ', vi xử lý {}'.format(cpu)
            if type(memory) is str:
                description += ', bộ nhớ {}'.format(memory)
            if type(screen) is str:
                description += ', màn hình {}'.format(screen)
            if type(card) is str and len(card) > 0:
                description += ', card đồ hoạ {}'.format(card)
            price = product.get('price')
            if type(price) is str:
                description += '. Giá bán {}'.format(price)

    if product['category'].lower() == 'Máy tính bảng'.strip().lower():
        description = 'Máy tính bảng {}'.format(product['name'])
        bginfo = product.get('bginfo')
        if type(bginfo) is dict:
            cpu = bginfo.get('CPU')
            memory = bginfo.get('RAM')
            camera = bginfo.get('Camera')
            screen = bginfo.get('Màn hình')
            if type(camera) is str:
                description += ' với camera {}'.format(camera)
            if type(screen) is str:
                description += ', màn hình {}'.format(screen)
            if type(memory) is str:
                description += ', bộ nhớ {}'.format(memory)
            if type(cpu) is str:
                description += ', vi xử lý {}'.format(cpu)
            price = product.get('price')
            if type(price) is str:
                description += '. Giá bán {}'.format(price)

    return description


@service.route('/find', methods=['POST'])
def find():
    request_info = request.get_json()
    category = request_info.get('category', None)
    name = request_info.get('name')
    brand = request_info.get('brand')
    properties = request_info.get('properties')

    try:
        max_price = int(request_info.get('max_price'))
    except:
        max_price = None
    try:
        min_price = int(request_info.get('min_price'))
    except:
        min_price = None

    product_model = Product()

    if category is not None:
        products = product_model.get_by_category(category)
    else:
        products = product_model.get_all()

    products = [_create_response_product(product) for product in products]

    if type(name) is str and len(name) > 0:
        name = name.strip().lower()
        products = [product for product in products if name in str(product['name']).lower()]

    if type(brand) is str and len(brand) > 0:
        brand = brand.strip().lower()
        products = [product for product in products if brand in str(product['name']).lower()]

    if type(max_price) is int:
        products = [product for product in products if product['price'] <= max_price]
    if type(min_price) is int:
        products = [product for product in products if product['price'] >= min_price]

    return_products = list()
    if type(properties) is dict:
        color = properties.get('color')
        if type(color) is str:
            for product in products:
                for c in product['colors']:
                    if color.lower() in c.lower():
                        try:
                            product['image'] = product['images'][c]
                        except:
                            pass
                        return_products.append(product)
        else:
            return_products = products
    else:
        return_products = products

    return jsonify({'products': return_products[:5]})


@service.route('/categories')
def get_categories():
    product_model = Product()
    categories = product_model.get_categories()
    return jsonify({'categories': categories})


@service.route('/category/<category_name>')
def get_product_by_category(category_name):
    product_model = Product()
    products = product_model.get_by_category(category_name)
    products = [_create_response_product(product) for product in products]
    return jsonify(products)


def _create_response_product(product):
    response_product = dict()
    if type(product) is not dict:
        return dict()
    response_product['name'] = product.get('name', '')
    response_product['category'] = product.get('category', '')
    response_product['productId'] = product.get('productId', '')

    try:
        price = product.get('price', '').replace('.', '').replace('₫', '')
        response_product['price'] = int(price)
    except:
        response_product['price'] = 0

    response_product['image'] = product.get('imgUrl', '')

    product_colors = list()
    colors = product.get('fullSaleInfo').get('colors')
    images = dict()

    for color in colors:
        product_colors += [colorname for colorname in color]
        for k, v in color.items():
            images[k] = v
    response_product['images'] = images
    colors = list()
    for color in product_colors:
        color = color.split('&')
        colors += [c.strip() for c in color]
    response_product['colors'] = colors

    return response_product
