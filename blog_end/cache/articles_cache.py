# 文章相关的缓存方法 ： 文章分类的读取和写入
#ket - value
from typing import List, Dict, Any, Optional

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY= "articles:categories"
ARTICLES_LIST_PREFIX = "articles_list:"



# #获取文章分类缓存
# async def get_cache_categories():
#     return await get_json_cache(CATEGORIES_KEY)
#
# #写入文章分类缓存：缓存的数据，过期时间
# async def set_cache_categories(data:List[Dict[str,Any]],expire:int = 7200):
#     return await set_cache(CATEGORIES_KEY, data,expire)


#写入缓存-文章列表 key = articles_list : 分类id：页码：每页数量 +列表数据 +过期时间
async def set_cache_articles_list(
        category_id:Optional[int],
        page:int,
        page_size:int,
        articles_list:List[Dict[str,Any]],
        expire : int = 1800
):
    """设置文章列表缓存"""
    #调用 封装的 Redis 的设置方法，存文章列表到缓存
    category_part = category_id if category_id is not None else "all"
    key = f"{ARTICLES_LIST_PREFIX}{category_part}:{page}:{page_size}"
    return await set_cache(key, articles_list, expire)


#读取缓存-文章列表
async def get_cache_articles_list(
        category_id:Optional[int],
        page:int,
        page_size:int
):
    """获取文章列表缓存"""
    # 构造缓存键并查询
    category_part = category_id if category_id is not None else "all"
    key = f"{ARTICLES_LIST_PREFIX}{category_part}:{page}:{page_size}"
    return await get_json_cache(key)

