# -*- coding:utf-8 -*-
import numpy as np
from scipy.special import gammaln, gamma


class MultinomialDistribution(object):
    def __init__(self, p, rso=np.random):
        if not np.isclose(np.sum(p), 1):
            raise ValueError("event probabilities do not sum to 1")
        self.p = p
        self.rso = rso
        self.log_p = np.log(self.p)

    def sample(self, n):
        return self.rso.multinomial(n, self.p)

    def log_pmf(self, x):
        n = np.sum(x)
        # log(n!)
        log_n_factorial = gammaln(n + 1)

        '''log(x1!*x2!*...*xk!) = log(x1!)+log(x2!)+...+log(xk!)
        '''
        log_xi_factorial = np.sum(gammaln([_ + 1 for _ in x]))

        """
            log(p1**x1 * p2**x2 * ... pk**xk) 
            = log(p1 ** x1) + log(p2 ** x2) + ... + log(pk ** xk) 
            = x1log(p1) + x2log(p2) +...+ xklog(pk)
        """
        log_p_xi = self.log_p * x
        log_p_xi[x == 0] = 0

        sum_log_p_xi = np.sum(log_p_xi)

        log_pmf_value = log_n_factorial - log_xi_factorial + sum_log_p_xi
        return log_pmf_value


if __name__ == '__main__':
    x = 5
    md = MultinomialDistribution(np.array([0.25, 0.25, 0.25, 0.25]))
    a = md.log_pmf([2, 0, 0, 0])
    print(a)
    print(np.exp(a))
    print(md.sample(1))

