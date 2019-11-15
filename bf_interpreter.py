from constants import Constants
from bf_exceptions import MismatchedBracketsError, MemoryOutOfBoundsError


class BfInterpreter:
    """
    An interpreter for Brainf***.
    By: Abhinna Adhikari
    Can go out of memory depending on the pointer.
    Reads the instructions from the file name found in the constants class.
    """
    def __init__(self):
        self._mem_cells = [0 for i in range(Constants.TOTAL_MEMORY_CELLS)]
        self._ptr = 0
        self._instructions_file_name = Constants.INSTRUCTIONS_FILE_NAME
        self._instructions = self._read_instruction_from_file()
        self._instruction_index = 0

    def _period(self):
        """
        Prints out the byte value of the current cell pointed to as ascii character.
        """
        print(chr(self._mem_cells[self._ptr]), end='')
        self._instruction_index += 1

    def _comma(self):
        """
        Takes only one byte of input from user and stores the byte value in the cell pointed to by the pointer.
        """
        self._mem_cells[self._ptr] = ord(input()[0])
        self._instruction_index += 1

    def _increment(self):
        """
        Increments the current cell that is being pointed to by one.
        """
        self._mem_cells[self._ptr] = (self._mem_cells[self._ptr] + 1) % (Constants.MAX_NUM + 1)
        self._instruction_index += 1

    def _decrement(self):
        """
        Decrements the current cell that is being pointed to by one.
        """
        self._mem_cells[self._ptr] = Constants.MAX_NUM if self._mem_cells[self._ptr] == 0 else self._mem_cells[self._ptr] - 1
        self._instruction_index += 1

    def _less_than(self):
        """
        Move the pointer one cell to the left.
        """
        self._ptr -= 1
        if self._ptr < 0:
            raise MemoryOutOfBoundsError
        self._instruction_index += 1

    def _greater_than(self):
        """
        Move the pointer one cell to the right.
        """
        self._ptr += 1
        if self._ptr > Constants.TOTAL_MEMORY_CELLS:
            raise MemoryOutOfBoundsError
        self._instruction_index += 1

    def _left_square_bracket(self):
        """
        If byte value of currently pointed cell is zero,
        then jump to the right of the matching right square bracket.
        Otherwise, move to the next instruction.
        """
        right_square_bracket = self._matching_right_square_bracket()
        self._instruction_index = right_square_bracket + 1 if self._mem_cells[self._ptr] == 0 else self._instruction_index + 1

    def _matching_right_square_bracket(self):
        """
        Finds the corresponding right square bracket of the current left square bracket.
        """
        temp_index = self._instruction_index
        bracket_count = 1
        while bracket_count > 0:
            temp_index += 1
            if temp_index >= len(self._instructions):
                raise MismatchedBracketsError
            if self._instructions[temp_index] == '[':
                bracket_count += 1
            elif self._instructions[temp_index] == ']':
                bracket_count -= 1
        return temp_index

    def _right_square_bracket(self):
        """
        If byte value of currently pointed cell is nonzero,
        then jump to the right of the matching left square bracket.
        Otherwise, move to the next instruction.
        """
        left_square_bracket = self._matching_left_square_bracket()
        self._instruction_index = left_square_bracket if self._mem_cells[self._ptr] != 0 else self._instruction_index + 1

    def _matching_left_square_bracket(self):
        """
        Finds the corresponding left square bracket of the current right square bracket.
        """
        temp_index = self._instruction_index
        bracket_count = 1
        while bracket_count > 0:
            temp_index -= 1
            if temp_index < 0:
                raise MismatchedBracketsError
            if self._instructions[temp_index] == ']':
                bracket_count += 1
            elif self._instructions[temp_index] == '[':
                bracket_count -= 1
        return temp_index

    def run_interpreter(self):
        """
        Goes through the instructions until the end is reached.
        """
        while self._instruction_index < len(self._instructions):
            bf_instr = self._instructions[self._instruction_index]
            if bf_instr is '+':
                self._increment()
            elif bf_instr is '-':
                self._decrement()
            elif bf_instr is '.':
                self._period()
            elif bf_instr is ',':
                self._comma()
            elif bf_instr is '<':
                self._less_than()
            elif bf_instr is '>':
                self._greater_than()
            elif bf_instr is '[':
                self._left_square_bracket()
            elif bf_instr is ']':
                self._right_square_bracket()
            else:
                # if none of the above, then is a comment which is ignored, so simply increment the instruction index
                self._instruction_index += 1

    def print_n_cells(self, n):
        """
        Prints cells from index 0 to index n - 1 of the memory cells onto the screen.
        If n is greater than the total length of the memory cells, then simply
        print the memory cell in its entirety
        """
        print(self._mem_cells[:n]) if n <= Constants.TOTAL_MEMORY_CELLS else print(self._mem_cells)

    def _read_instruction_from_file(self):
        """
        Gets the Brainf*** instructions from the file name found in the constants class
        """
        with open(self._instructions_file_name) as r:
            return r.read().replace('\n', '').replace(' ', '')

if __name__ == '__main__':
    bfi = BfInterpreter()
    bfi.run_interpreter()
