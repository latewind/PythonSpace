from multidist import MultinomialDistribution
import numpy as np


class MagicItemDistribution(object):
    STATS_NAME = ["气血", "力量", "灵力", "防御", "敏捷"]

    def __init__(self, bonus_probs, stats_probs, rso=np.random):
        self.bonus_probs = bonus_probs
        self.stats_probs = stats_probs

        self.bonus_dist = MultinomialDistribution(bonus_probs)
        self.stats_dist = MultinomialDistribution(stats_probs)

    def _sample_bonus(self):
        bonus = self.bonus_dist.sample(1)
        return np.argmax(bonus)

    def _sample_stats(self):
        bonus = self._sample_bonus()
        stats = self.stats_dist.sample(bonus)
        return stats

    def sample(self):
        stats = self._sample_stats()
        item_stats = dict(zip(self.STATS_NAME, stats))
        return item_stats

    def pmf(self, log_pmf):
        return np.exp(log_pmf)

    def log_pmf(self, item):
        stats = np.array([item[stats_name] for stats_name in self.STATS_NAME])
        stats_log_pmf = self.stats_dist.log_pmf(stats)
        total_bonus = np.sum(stats)
        bonus_log_pmf = self._bonus_log_pmf(total_bonus)
        return stats_log_pmf + bonus_log_pmf

    def _bonus_log_pmf(self, total_bonus):
        bonus = np.zeros(len(self.bonus_probs))
        bonus[total_bonus] = 1
        return self.bonus_dist.log_pmf(bonus)


if __name__ == '__main__':
    md = MagicItemDistribution([0.55, 0.25, 0.12, 0.06, 0.02], [.25, .25, .2, .2, .1])
    item = md.sample()
    log_pmf = md.log_pmf(item)
    pmf = md.pmf(log_pmf)
    print(item)
    print(log_pmf)
    print(pmf)

