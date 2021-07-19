from app import es, es_index2


# def insert(data: dict):
#     es.index(index=es_index, body=data)
#
#
# def query(data: dict):
#     body = {
#         "query": {
#             "match": data
#         }
#     }
#     s_list = es.search(index=es_index, body=body)
#     # 数据
#     data_list = []
#     # 对应 id
#     id_list = []
#     for hit in s_list.get('hits').get('hits'):
#         data_list.append(hit.get('_source'))
#         id_list.append(hit.get('_id'))
#     return id_list, data_list
#
#
# def update(data: dict, cid: str):
#     body = {
#         "doc": data
#     }
#     es.update(index=es_index, id=cid, body=body)
#
#
# def delete(data: dict):
#     body = {
#         "query": {
#             "match": data
#         }
#     }
#     return es.delete_by_query(index=es_index, body=body)


def query2(data: dict):
    # 构造检索参数
    body = {
        "query": {
            "match": data
        }
    }
    # 调用ES
    s_list = es.search(index=es_index2, body=body)
    # 数据
    data_list = []
    # 对应 id
    id_list = []
    # 处理检索结果
    for hit in s_list.get('hits').get('hits'):
        data_list.append(hit.get('_source'))
        id_list.append(hit.get('_id'))
    return id_list, data_list


def insert2(data: dict):
    es.index(index=es_index2, body=data)


def delete2(data: dict):
    body = {
        "query": {
            "match": data
        }
    }
    return es.delete_by_query(index=es_index2, body=body)
