import math


class LogUniform:
    def __init__(self, popular_dict, **kwargs):
        """
        :param popular_dict: dict
        :param kwargs:
        """
        super(LogUniform, self).__init__(**kwargs)
        self.popular_dict = popular_dict
        self.item_scores = {}
        self.item_score_ranked = {}
        self.max_rank = 0
        self.item_log_uniform = {}
        self.item_prob_distributions_dict = {}
        self.item_prob_distributions_list = [0]

    def get_item_score(self):
        """item打分
        :return:
        """
        for item, info in self.popular_dict.items():
            self.item_scores[item] = info

    def get_item_rank(self):
        """
        :return:
        """
        # 从高到低给item_scores排序
        item_score_sorted = sorted(self.item_scores.items(), key=lambda d: d[1], reverse=True)
        # 按分数从高到低获得每个item的排名
        for i in range(len(item_score_sorted)):
            self.item_score_ranked[item_score_sorted[i][0]] = i
        self.max_rank = len(self.item_score_ranked)
        return self.item_score_ranked

    @staticmethod
    def log_uniform(k, D):
        """https://arxiv.org/pdf/1906.05022.pdf
        :param k:
        :param D:
        :return:
        """
        return (math.log(k + 2) - math.log(k + 1)) / math.log(D + 1)

    def get_log_uniform(self):
        """
        :return:
        """
        self.item_log_uniform = {item: LogUniform.log_uniform(rank, D=self.max_rank) for item, rank in
                                 self.item_score_ranked.items()}
        return self.item_log_uniform

    def get_probability_distributions(self):
        """获得概率分布
        :return:
        """
        first = True
        for k, v in self.item_log_uniform.items():
            if first:
                self.item_prob_distributions_dict[k] = str([0, v])
                pre = v
                first = False
            else:
                self.item_prob_distributions_dict[k] = str([pre, pre + v])
                pre = pre + v
            self.item_prob_distributions_list.append(pre)
        self.item_prob_distributions_dict = dict(
            zip(self.item_prob_distributions_dict.values(), self.item_prob_distributions_dict.keys()))
        return self.item_prob_distributions_list, self.item_prob_distributions_dict

    def find_interval(self, key, arrays):
        low, high = 0, len(arrays) - 1
        while low <= high:
            mid = (low + high) // 2
            if arrays[mid] < key:
                low = mid + 1
            elif arrays[mid] > key:
                high = mid - 1
            else:
                break
        if low < high:
            return [arrays[low], arrays[high]]
        else:
            return [arrays[high], arrays[low]]
