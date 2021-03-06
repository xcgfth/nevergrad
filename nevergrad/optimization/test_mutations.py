# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import numpy as np
from ..common import testing
from . import utils
from .mutations import Mutator


def test_discrete_mutation() -> None:
    data = [0.1, -.1, 1]
    rng = np.random.RandomState(12)
    output = Mutator(rng).discrete_mutation(data)
    np.testing.assert_almost_equal(output, [-.33, -.1, .02], decimal=2)


def test_crossover() -> None:
    data = [0.1, -.1, 1, -0.1]
    rng = np.random.RandomState(15)
    output = Mutator(rng).crossover(data, 2 * np.array(data))
    np.testing.assert_almost_equal(output, [-1.1, -.1, 2, -.1], decimal=2)


@testing.parametrized(
    dicrete=("discrete_mutation",),
    portfolio_discrete=("portfolio_discrete_mutation",),
    doubledoerr=("doubledoerr_discrete_mutation",),
    doerr=("doerr_discrete_mutation",),
)
def test_run_with_array(name: str) -> None:
    data = [0.1, -.1, 1, -.2] * 3
    mutator = Mutator(np.random.RandomState(12))
    func = getattr(mutator, name)
    output1 = func(data)
    mutator.random_state.seed(12)
    output2 = func(np.array(data))
    np.testing.assert_equal(output1, output2)


@testing.parametrized(
    only_2=(2, 1.5),
    all_4=(4, 0.5),
)
def test_get_roulette(num: int, expected: str) -> None:
    rng = np.random.RandomState(24)
    archive = utils.Archive[utils.Value]()
    for k in range(4):
        archive[np.array([k + .5])] = utils.Value(k)
    output = Mutator(rng).get_roulette(archive, num)
    np.testing.assert_equal(output, expected)
