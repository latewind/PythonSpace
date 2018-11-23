from magicdist import MagicItemDistribution
from multidist import MultinomialDistribution
import numpy as np
import matplotlib.pyplot as plt

class DamageDistribution(object):
    def __init__(self, num_item, item_dist, num_dice_sides=12, num_hits=3):
        self.num_item = num_item
        self.dice_sides = np.arange(1, num_dice_sides + 1)
        self.multi_dist = MultinomialDistribution(np.ones(num_dice_sides) / float(num_dice_sides))
        self.item_dist = item_dist
        self.num_hits = num_hits

    def sample(self):
        item = [self.item_dist.sample() for _ in np.arange(1, self.num_item + 1)]
        dice_num = 1 + np.sum([i["力量"] for i in item])
        dice_rolls = self.multi_dist.sample(dice_num * self.num_hits)
        damage = np.sum(dice_rolls * self.dice_sides)
        return damage


if __name__ == '__main__':
    item_dist = MagicItemDistribution([0.55, 0.25, 0.12, 0.06, 0.02], [.25, .25, .2, .2, .1])
    damage_dist = DamageDistribution(2, item_dist)
    samples = np.array([damage_dist.sample() for i in range(10000)])
    #print(samples)
    #np.percentile(samples, 50)
    #plt.hist(samples)
    #plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, rectangles = ax.hist(samples, 50,density=False)
    fig.canvas.draw()
    plt.show()
