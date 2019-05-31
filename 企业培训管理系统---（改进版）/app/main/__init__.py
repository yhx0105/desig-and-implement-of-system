from flask import Blueprint

main = Blueprint('main', __name__)

from ..models import Permission
# 把路由与exception程序与蓝本关联起来,所以他们的路由都由蓝本提供
from . import views, errors


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)



