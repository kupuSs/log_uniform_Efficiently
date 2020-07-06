import random
import time
import pandas as pd
from collections import Counter

import log_uniform

fruits_dict = {  # 模拟水果的售卖数量
    'apple': 16,
    'banana': 70,
    'watermelon': 29,
    'mango': 10,
    'peach': 40,
    'orange': 1020,
    'pear': 5,
    'strawberry': 2030,
    'olive': 24,
    'lemon': 9990
}

SAMPLING_NUMS = 1000000

if __name__ == '__main__':
    # log_uniform
    lu = log_uniform.LogUniform(popular_dict=fruits_dict)
    lu.get_item_score()  # 给每个item打分
    lu.get_item_rank()  # 按分数从高到低获得每个item的排名
    lu.get_log_uniform()  # 获得log_uniform概率
    item_prob_dist_list, item_prob_dist_dict = lu.get_probability_distributions()  # 获取log_uniform概率分布

    start = time.time()
    fruits_log_uniform_list = []
    for _ in range(SAMPLING_NUMS):
        key = random.random()  # 先通过均匀分布产生一个[0,1]内的概率
        key_interval = lu.find_interval(key=key, arrays=item_prob_dist_list)  # 查找key所在的概率分布区间
        neg_item = item_prob_dist_dict[str(key_interval)]  # 该区间即为对应的negative item
        fruits_log_uniform_list.append(neg_item)
    print('log uniform sampling {} cost time: {} sec'.format(SAMPLING_NUMS, time.time() - start))

    fruits_log_uniform_ranked = sorted(Counter(fruits_log_uniform_list).items(), key=lambda d: d[1], reverse=True)

    # random
    fruits_list = []
    for k, v in fruits_dict.items():
        fruits_list.extend([k] * v)
    random.shuffle(fruits_list)

    start = time.time()
    fruits_random_list = []
    for _ in range(SAMPLING_NUMS):
        neg_item = random.sample(fruits_list, 1)[0]
        fruits_random_list.append(neg_item)
    print('random sampling {} cost time: {} sec'.format(SAMPLING_NUMS, time.time() - start))

    fruits_random_ranked = sorted(Counter(fruits_random_list).items(), key=lambda d: d[1], reverse=True)

    df = pd.DataFrame(
        index=[fruits_random_ranked[i][0] for i in range(len(fruits_dict))],
        columns=['random', 'log uniform'])

    df['random'] = [fruits_random_ranked[i][1]/SAMPLING_NUMS for i in range(len(fruits_dict))]
    df['log uniform'] = [fruits_log_uniform_ranked[i][1]/SAMPLING_NUMS for i in range(len(fruits_dict))]
    print(df)
