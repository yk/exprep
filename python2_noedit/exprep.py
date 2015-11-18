from __future__ import absolute_import
from typing import Callable, List, Dict, Tuple
import numpy as np
from itertools import izip


class Experiment(object):
    def perform(self):
        pass


def as_experiment(experiment_callable):
    return type(u"AdHocExperiment", (Experiment,), {u"perform": lambda self: experiment_callable()})()


def transpose_list_of_dict(repetitions):
    d = dict()
    for rd in repetitions:
        for k, v in rd.items():
            if k not in d:
                d[k] = []
            d[k].append(v)
    return d


class RepetitionsCombiner(object):
    def combine(self, repetitions):
        pass


class DummyCombiner(RepetitionsCombiner):
    def combine(self, repetitions):
        return repetitions[0]


class KeyWiseRepetitionsCombiner(RepetitionsCombiner):
    def combine_key(self, key, repetitions):
        pass

    def combine(self, repetitions):
        d = transpose_list_of_dict(repetitions)
        return dict((k, self.combine_key(k, v)) for k, v in d.items())


class AverageCombiner(KeyWiseRepetitionsCombiner):
    def combine_key(self, key, repetitions):
        return tuple(np.mean(a, axis=0) for a in izip(*repetitions))


class AverageAndStdCombiner(KeyWiseRepetitionsCombiner):
    def combine_key(self, key, repetitions):
        return tuple((np.mean(a, axis=0), np.std(a, axis=0)) for a in izip(*repetitions))


def as_combiner(experiment_callable):
    return type(u"AdHocRepetitionsCombiner", (RepetitionsCombiner,), {u"combine": lambda self: experiment_callable()})()


def repeat_experiment(experiment, repetitions = 5):
    results = []
    for _ in xrange(repetitions):
        results.append(experiment.perform())
    return results


def combine_results(results, combiner = None):
    if combiner is None:
        combiner = DummyCombiner()
    return combiner.combine(results)


def repeat_and_combine_experiment(experiment, combiner, repetitions = 5):
    return combine_results(repeat_experiment(experiment, repetitions), combiner)
