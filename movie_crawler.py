from vieshow import vieshow
from universal import universal
import pickle
import pprint
from mongoDAO import mongodb_for_data

# 先各自用release_date 排序
# if release_data 一樣，origin_title 不重複，直接取出
# elif release_data 一樣，origin_title 重複，將所有key 拿出比較，
# 合併source
# if key 不重複，直接取出
# elif key 重複
# 將!= None 的資料，取代None
# 其他使用威秀資料


def main():
    # vieshow_movie_data = vieshow.Vieshow()
    # universal_movie_data = universal.perpage()
    # with open('./test_data/vieshow_coming.pk', 'wb') as f:
    #     pickle.dump(vieshow_movie_data, f)
    # with open('./test_data/universal_movie_data.pk', 'wb') as f:
    #     pickle.dump(universal_movie_data, f)
    # return

    # with open('./test_data/vieshow_coming.pk', 'rb') as f:
    #    vieshow_data = pickle.load(f)
    # with open('./test_data/universal_movie_data.pk', 'rb') as f:
    #    universal_data = pickle.load(f)

    #movie_list = compare_two_list(vieshow_data, universal_data)
    mongo = mongodb_for_data.MongoDb()
    mongo.connection()
    mongo.find_max_movie_id()
    for movie in vieshow_data:
        exist_in_mongo = []
        title_str = ''.join(e for e in movie['origin_title'] if e.isalnum())
        title_str = title_str.lower()
        for doc in mongo.find(movie['release_date'], title_str):
            exist_in_mongo.append(compare_element(doc, movie))
        if len(exist_in_mongo) != 0:
            #        mongo.insert(exist_in_mongo[0])
            print('exist:\n', exist_in_mongo[0])
        else:
            #        mongo.insert(movie)
            print('not exist:\n', movie)


def compare_two_list(list1, list2):
    # 將電影資料合併
    list1.extend(list2)
    total_data = list1

    # 依照上映時間排序
    sorted_data = list_sorter(total_data)

    # 取出所有上映時間，並去除重複
    # 並且依照release_date 分組成二維矩陣
    date = [dicts['release_date'] for dicts in sorted_data]
    date_clean = []
    for day in date:
        if day not in date_clean:
            date_clean.append(day)
    group_by_date = []
    for day in date_clean:
        group_by_date.append(
            list(filter(lambda x: x['release_date'] == day, sorted_data)))

    # 相同上映時間，如果origin_title不重複就整筆取出，若重複進行比較
    final_movie_list = []
    for movie_list in group_by_date:
        final_movie_list.extend(which_movie(movie_list))

    return final_movie_list


def list_sorter(row_list):
    new_list = sorted(row_list, key=lambda x: x['release_date'])
    return new_list


def which_movie(mlist):
    result = []
    title = []
    for movie in mlist:
        # 去除英文以及數字以外字元，並取小寫
        title_str = ''.join(e for e in movie['origin_title'] if e.isalnum())
        title_str = title_str.lower()
        if title_str not in title:
            title.append(title_str)
            result.append(movie)
        else:
            # 當前電影，與當前director 已存在的電影比
            exist = title.index(title_str)
            result[exist] = compare_element(movie, result[exist])
    return result


# 比較origin_title 跟發行日期一樣的資料
def compare_element(dict1, dict2):
    key_list1 = list(dict1.keys())
    key_list2 = list(dict2.keys())
    total_keys = list(set(key_list1 + key_list2))
    result_dict = {}
    for key in total_keys:
        try:
            print(dict1[key])
        except KeyError:
            dict1[key] = None
        try:
            print(dict2[key])
        except KeyError:
            dict2[key] = None
        if dict1[key] == None and dict2[key] != None:
            result_dict[key] = dict2[key]
        elif dict1[key] != None and dict2[key] == None:
            result_dict[key] = dict1[key]
        elif dict1[key] == None and dict2[key] == None:
            result_dict[key] = None
        else:
            result_dict[key] = which_value(key, dict1, dict2)

    print('-' * 50)
    return result_dict


# 同一key 的value 間做選擇
def which_value(key, dict1, dict2):
    # value 一樣
    if dict1[key] == dict2[key]:
        return dict1[key]
    # value 不一樣
    else:
        if key == 'content':
            return dict1[key] + dict2[key]
        elif key == 'source':
            dict1[key].extend(dict2[key])
            return dict1[key]
        elif key == 'image_path':
            dict1[key].extend(dict2[key])
            return dict1[key]
        elif key == 'poster_path':
            dict1[key].extend(dict2[key])
            return dict1[key]
        elif key == 'cast':
            if len(dict1[key]) >= len(dict2[key]):
                return dict1[key]
            else:
                return dict2[key]
        elif key == 'director':
            if len(dict1[key]) >= len(dict2[key]):
                return dict1[key]
            else:
                return dict2[key]
        else:
            return dict1[key]


if __name__ == '__main__':
    main()
