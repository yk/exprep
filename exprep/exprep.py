import numpy as np


class Experiment:
    def perform(self) -> list:
        pass


def as_experiment(experiment_callable):
    return type("AdHocExperiment", (Experiment,), {"perform": lambda self: experiment_callable()})()


def transpose_list_of_dict(repetitions):
    d = dict()
    for rd in repetitions:
        for k, v in rd.items():
            if k not in d:
                d[k] = []
            d[k].append(v)
    return d


class RepetitionsCombiner:
    def combine(self, repetitions: list) -> dict:
        pass


class DummyCombiner(RepetitionsCombiner):
    def combine(self, repetitions: list):
        return repetitions[0]


class KeyWiseRepetitionsCombiner(RepetitionsCombiner):
    def combine_key(self, key: str, repetitions: list) -> tuple:
        pass

    def combine(self, repetitions: list):
        d = transpose_list_of_dict(repetitions)
        return {k: self.combine_key(k, v) for k, v in d.items()}


class AverageCombiner(KeyWiseRepetitionsCombiner):
    def combine_key(self, key: str, repetitions: list) -> tuple:
        return tuple(np.mean(a, axis=0) for a in zip(*repetitions))


class AverageAndStdCombiner(KeyWiseRepetitionsCombiner):
    def combine_key(self, key: str, repetitions: list) -> tuple:
        return tuple((np.mean(a, axis=0), np.std(a, axis=0)) for a in zip(*repetitions))


def as_combiner(experiment_callable):
    return type("AdHocRepetitionsCombiner", (RepetitionsCombiner,), {"combine": lambda self: experiment_callable()})()


def repeat_experiment(experiment: Experiment, repetitions: int = 5):
    results = []
    for _ in range(repetitions):
        results.append(experiment.perform())
    return results


def combine_results(results: list, combiner: RepetitionsCombiner = None):
    if combiner is None:
        combiner = DummyCombiner()
    return combiner.combine(results)


def repeat_and_combine_experiment(experiment: Experiment, combiner: RepetitionsCombiner, repetitions: int = 5):
    return combine_results(repeat_experiment(experiment, repetitions), combiner)
