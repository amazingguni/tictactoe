import numpy as np
import pytest


@pytest.fixture
def g():
    return Game()


class IllegalPosition(Exception):
    pass


class Game(object):
    def __init__(self):
        self.state = np.zeros(9)

    def get_user_input(self, test_input=None):
        """Get user input.

        @Args:
            test_input: Test input

        @Returns:
            int: Index of input position.

        @Raises:
            IllegalPosition
        """
        idx = None
        if test_input is not None:
            inp = test_input
        else:
            inp = input(self.user_input_prompt())
        try:
            idx = int(inp) - 1
        except ValueError:
            raise IllegalPosition()

        if idx < 0 or idx > 8:
            raise IllegalPosition()

        if idx not in self.get_legal_index():
            raise IllegalPosition()

        return idx

    def user_input_prompt(self):
        return "Enter position[1-9]: "

    def draw(self):
        rv = '\n'
        for y in range(3):
            for x in range(3):
                idx = y * 3 + x
                t = self.state[idx]
                if t == 1:
                    rv += 'X'
                elif t == 2:
                    rv += 'O'
                else:
                    if x < 2:
                        rv += ' '
                if x < 2:
                    rv += '|'
            rv += '\n'
            if y < 2:
                rv += '-----\n'
        return rv

    def get_legal_index(self):
        return np.nonzero(np.equal(0, self.state))[0].tolist()


def test_draw(g):
    assert g.draw() == '''
 | |
-----
 | |
-----
 | |
'''
    assert len(g.state) == 9

    # 1|2|3
    # -----
    # 4|5|6
    # -----
    # 7|8|9
    #
    # X: 1, O: 2
    pos = 1
    idx = pos - 1
    g.state[idx] = 2
    assert g.draw() == '''
O| |
-----
 | |
-----
 | |
'''
    pos = 9
    idx = pos - 1
    g.state[idx] = 1
    assert g.draw() == '''
O| |
-----
 | |
-----
 | |X
'''


def test_user_input(g):
    assert g.user_input_prompt() == "Enter position[1-9]: "
    with pytest.raises(IllegalPosition):
        g.get_user_input('eueueu')
    with pytest.raises(IllegalPosition):
        g.get_user_input('0')
    with pytest.raises(IllegalPosition):
        g.get_user_input('10')

    g.state[0] = 1
    with pytest.raises(IllegalPosition):
        g.get_user_input('1')

def test_legal_positions(g):
    assert g.get_legal_index() == [0, 1, 2, 3, 4, 5, 6, 7, 8,]
    g.state[0] = 1
    assert g.get_legal_index() == [1, 2, 3, 4, 5, 6, 7, 8]
    g.state[8] = 2
    assert g.get_legal_index() == [1, 2, 3, 4, 5, 6, 7]
