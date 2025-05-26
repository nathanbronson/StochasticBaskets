from random import sample
from copy import copy
from math import exp
from functools import partial

import numpy as np
from tqdm import tqdm
from joblib.parallel import delayed, Parallel

from common import Team, WinMatrix, Bracket
from mcmc import MetropolisHastingsBracket
from utils import bracket_idx_to_overall, naive_bracket

class Seeding:
    def __init__(self, teams: list[Team], win_matrix: WinMatrix):
        assert len(teams) == 64
        self.teams = teams
        self.seed: dict[Team, int] = {t: n for n, t in enumerate(self.teams)}
        self.win_matrix = win_matrix
        self.mlb = None
        self._score = None
        self.dist = None
    
    def __str__(self) -> str:
        return "\n".join(map(lambda x: "(" + str(1 + x[0]//4) + ") " + x[1].name, enumerate(self.teams)))
    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        result.teams = copy(result.teams)
        
        return result
    
    def __hash__(self):
        return hash(tuple(self.teams))

    def find_maximimum_likelihood_bracket(self, iters: int = 1500, verbose: bool = True) -> Bracket:
        mhb = MetropolisHastingsBracket(Seeding.arrange(self.teams), win_matrix=self.win_matrix, simulate_anneal=True)
        self.mlb = mhb.run(iters=iters, verbose=verbose)[-1]
        return self.mlb
    
    def mean_variance(self, iters: int = 100000, verbose: bool = True) -> float:
        mhb = MetropolisHastingsBracket(Seeding.arrange(self.teams), win_matrix=self.win_matrix, simulate_anneal=False)
        self.dist = [-i.depth_error() for i in mhb.run(iters=iters, verbose=verbose)]
        
        return np.mean(self.dist) - np.std(self.dist)
    
    def score(self, iters: int = 6000, reps: int = 9, verbose: bool = False, exponential_score: bool = False) -> float:
        if self._score is not None:
            return self._score
        self._score = 0
        scores = Parallel(n_jobs=-1)(delayed(partial(self.mean_variance, iters=iters, verbose=verbose))() for _ in range(reps))
        self._score = sum(scores)
        
        
            
        self._score /= reps
        return self._score
    
    def random_transpose(self, limit: bool = True):
        idx1 = sample(range(len(self.teams)), 1)[0]
        idx2 = sample(range(max(0, idx1 - 5), min(idx1 + 5, len(self.teams))), 1)[0] if limit else sample(range(len(self.teams)), 1)[0]
        t1 = self.teams[idx1]
        t2 = self.teams[idx2]
        self.teams[idx1] = t2
        self.teams[idx2] = t1
        self._score = None
        return self
    
    def prepare_pickle(self):
        if hasattr(self.win_matrix, "prob_func"):
            del self.win_matrix.prob_func
        if self.mlb is not None:
            self.mlb.prepare_pickle()
        return self
    
    @classmethod
    def arrange(cls, teams: list[Team]) -> list[Team]:
        return [teams[bracket_idx_to_overall[i]] for i in range(64)]
    
    @classmethod
    def inverse_arrange(cls, teams: list[Team]) -> list[Team]:
        return [teams[{v: k for k, v in bracket_idx_to_overall.items()}[i]] for i in range(64)]
    
    @classmethod
    def RandomSeeding(cls, teams: list[Team], win_matrix: WinMatrix):
        return cls(sample(teams, len(teams)), win_matrix)

class MetropolisHastingsSeedings:
    def __init__(self, teams: list[Team], win_matrix: WinMatrix, seed_real: bool = False, T: float = None, alpha: float = None):
        self.teams = teams
        self.W = win_matrix
        self.x0: Seeding = Seeding(Seeding.inverse_arrange(naive_bracket()), self.W)
        self.X: list[Seeding] = [self.x0]
        self.T = T or 10
        self.alpha = alpha or .9995
        self.T_min = 1
    
    def _run_iter(self, anneal: bool = False, real_anneal: bool = False):
        b = self.X[-1]
        if real_anneal:
            self.X.append(self.real_anneal_accept(copy(b), copy(b).random_transpose()))
        elif anneal:
            self.X.append(self.anneal_accept(copy(b), copy(b).random_transpose()))
        else:
            self.X.append(MetropolisHastingsSeedings.accept(copy(b), copy(b).random_transpose()))
    
    def run(self, iters: int = 1000, verbose: bool = True, anneal: bool = False, real_anneal: bool = False):
        if verbose:
            for _ in (pbar := tqdm(range(iters))):
                self._run_iter(anneal=anneal, real_anneal=real_anneal)
                pbar.set_description_str("score: {}".format(self.X[-1].score()))
        else:
            for _ in range(iters):
                self._run_iter(anneal=anneal, real_anneal=real_anneal)
        return self.X
    
    def compute_mode(self, burnin: int = 0) -> Seeding:
        mp = {}
        _c = {}
        for x in self.X[burnin:]:
            h = hash(x)
            if h in mp:
                _c[h] += 1
            else:
                mp[h] = x
                _c[h] = 1
        return mp[list(_c.keys())[np.argmax(list(_c.values()))]]
    
    def real_anneal_accept(self, i: Seeding, j: Seeding, extremity: float = 1) -> Seeding:
        self.T = max(self.alpha * self.T, 1e-50)
        delta = (j.score(exponential_score=False) - i.score(exponential_score=False))
        print(exp(delta/self.T), j.score(exponential_score=False), i.score(exponential_score=False))
        if delta > 0: 
            
            
            return j
        else: 
            u = np.random.uniform(0, 1, 1)[0]
            
            
            if u < exp(delta/self.T):
                
                return j
            else:
                
                return i

    def anneal_accept(self, i: Seeding, j: Seeding, extremity: float = 1) -> Seeding:
        self.T = max(self.alpha * self.T, 1e-50)
        if len(self.X) > 500:
            if sample([True, False], counts=[1, 500], k=1)[0]:
                if sample([True, False], counts=[20, 80], k=1)[0]:
                    return sample(self.X, k=1)[0]
                else:
                    for _ in range(sample(range(10), k=1)[0]):
                        i.random_transpose()
                    return i.random_transpose()
        delta = (j.score(exponential_score=False) - i.score(exponential_score=False))
        print(exp(delta/self.T), j.score(exponential_score=False), i.score(exponential_score=False))
        if delta > 0: 
            
            
            return j
        else: 
            u = np.random.uniform(0, 1, 1)[0]
            
            
            if u < exp(delta/self.T):
                
                return j
            else:
                
                return i

    @classmethod
    def accept(cls, i: Seeding, j: Seeding, extremity: float = 1) -> Seeding:
        p = (j.score()/i.score()) ** extremity
        if p >= 1:
            return j
        return np.random.choice((j, i), p=(p, 1-p))