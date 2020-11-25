import redis


RID_URL = 'https://api.bilibili.com/x/web-interface/ranking/v2?rid={}&type={}'
LIST_URL = 'https://api.bilibili.com/pgc/season/rank/web/list?day=3&season_type={}'
NEW_LIST_URL = 'https://api.bilibili.com/pgc/web/rank/list?day=3&season_type={}'

rank_type_dict = {
    '全站': '0',
    '番剧': '1',
    '国产动画': '4',
    '国创相关': '168',
    '纪录片': '3',
    '动画': '1',
    '音乐': '3',
    '舞蹈': '129',
    '游戏': '4',
    '知识': '36',
    '数码': '188',
    '生活': '160',
    '美食': '211',
    '鬼畜': '119',
    '时尚': '155',
    '娱乐': '5',
    '影视': '181',
    '电影': '2',
    '电视剧': '5',
    '原创': '0',
    '新人': '0',
}
list_rank_types = [
    '番剧',  # list
    '国产动画',  # list
    '纪录片',  # list
    '电影',  # list
    '电视剧',  # list
]

client = redis.StrictRedis()
redis_key = 'rank:start_urls'


def push_url():
    """循环生成每种分类的url，插入到redis中"""
    for rank_type, rank_id in rank_type_dict.items():
        if rank_type == '原创':
            url = RID_URL.format(rank_id, 'origin')
        elif rank_type == '新人':
            url = RID_URL.format(rank_id, 'rookie')
        elif rank_type in list_rank_types:
            if rank_type != '番剧':
                url = LIST_URL.format(rank_id)
            else:
                url = NEW_LIST_URL.format(rank_id)
                # print('番剧url', url)
        else:
            url = RID_URL.format(rank_id, 'all')
        client.lpush(redis_key, url)


if __name__ == '__main__':
    push_url()

