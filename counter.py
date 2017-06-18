#!/usr/bin/env python
import struct
from collections import namedtuple
import itertools
import functools

SUM = 0
SUB = 1
RECURSIVE = 2

Register = namedtuple('Register', ['number', 'instruction', 'entry', 'left_next', 'right_next'])

def new_table(initial_value):
    return tuple([initial_value] + list(itertools.repeat(0, 25)))

@functools.lru_cache(maxsize=1048576)
def update_entry(table, entry, new_value):
    assert entry < len(table)

    return table[:entry] + (new_value,) + table[entry+1:]

@functools.lru_cache(maxsize=33554432)
def process_registers(registers, index, table):
    while True:
        if index >= len(registers):
            return table

        reg = registers[index]

        if reg.instruction == SUM:
            table = update_entry(table, reg.entry, table[reg.entry] + 1)
            index = reg.left_next

        elif reg.instruction == SUB:
            if table[reg.entry] != 0:
                table = update_entry(table, reg.entry, table[reg.entry] - 1)
                index = reg.left_next
            else:
                index = reg.right_next

        else:
            if reg.entry > 0:
                new_table = process_registers(registers, reg.left_next, table)

                for i in range(reg.entry):
                    table = update_entry(table, i, new_table[i])

            index = reg.right_next


if __name__ == '__main__':
    import sys
    registers = (
        Register(number=0, instruction=1, entry=0, left_next=1, right_next=2),
        Register(number=1, instruction=0, entry=1, left_next=0, right_next=0),
        Register(number=2, instruction=0, entry=2, left_next=3, right_next=0),
        Register(number=3, instruction=0, entry=2, left_next=4, right_next=0),
        Register(number=4, instruction=0, entry=2, left_next=5, right_next=0),
        Register(number=5, instruction=0, entry=2, left_next=6, right_next=0),
        Register(number=6, instruction=0, entry=2, left_next=7, right_next=0),
        Register(number=7, instruction=0, entry=2, left_next=8, right_next=0),
        Register(number=8, instruction=0, entry=2, left_next=9, right_next=0),
        Register(number=9, instruction=0, entry=2, left_next=10, right_next=0),
        Register(number=10, instruction=0, entry=2, left_next=11, right_next=0),
        Register(number=11, instruction=0, entry=2, left_next=12, right_next=0),
        Register(number=12, instruction=0, entry=2, left_next=13, right_next=0),
        Register(number=13, instruction=2, entry=1, left_next=108, right_next=14),
        Register(number=14, instruction=1, entry=0, left_next=119, right_next=15),
        Register(number=15, instruction=2, entry=1, left_next=20, right_next=16),
        Register(number=16, instruction=1, entry=2, left_next=16, right_next=17),
        Register(number=17, instruction=1, entry=0, left_next=18, right_next=19),
        Register(number=18, instruction=0, entry=2, left_next=17, right_next=0),
        Register(number=19, instruction=2, entry=1, left_next=64, right_next=119),
        Register(number=20, instruction=1, entry=2, left_next=20, right_next=21),
        Register(number=21, instruction=2, entry=1, left_next=29, right_next=22),
        Register(number=22, instruction=1, entry=0, left_next=23, right_next=24),
        Register(number=23, instruction=0, entry=2, left_next=22, right_next=0),
        Register(number=24, instruction=1, entry=1, left_next=25, right_next=26),
        Register(number=25, instruction=1, entry=25, left_next=0, right_next=21),
        Register(number=26, instruction=1, entry=0, left_next=26, right_next=27),
        Register(number=27, instruction=1, entry=2, left_next=28, right_next=119),
        Register(number=28, instruction=0, entry=0, left_next=27, right_next=0),
        Register(number=29, instruction=1, entry=2, left_next=29, right_next=30),
        Register(number=30, instruction=2, entry=1, left_next=84, right_next=31),
        Register(number=31, instruction=1, entry=3, left_next=31, right_next=32),
        Register(number=32, instruction=1, entry=0, left_next=33, right_next=34),
        Register(number=33, instruction=0, entry=3, left_next=32, right_next=0),
        Register(number=34, instruction=1, entry=3, left_next=35, right_next=42),
        Register(number=35, instruction=1, entry=3, left_next=36, right_next=42),
        Register(number=36, instruction=2, entry=1, left_next=45, right_next=37),
        Register(number=37, instruction=0, entry=2, left_next=38, right_next=0),
        Register(number=38, instruction=1, entry=1, left_next=38, right_next=39),
        Register(number=39, instruction=1, entry=0, left_next=40, right_next=41),
        Register(number=40, instruction=0, entry=1, left_next=39, right_next=0),
        Register(number=41, instruction=1, entry=25, left_next=0, right_next=30),
        Register(number=42, instruction=1, entry=0, left_next=42, right_next=43),
        Register(number=43, instruction=1, entry=2, left_next=44, right_next=119),
        Register(number=44, instruction=0, entry=0, left_next=43, right_next=0),
        Register(number=45, instruction=1, entry=2, left_next=45, right_next=46),
        Register(number=46, instruction=2, entry=1, left_next=84, right_next=47),
        Register(number=47, instruction=1, entry=0, left_next=48, right_next=49),
        Register(number=48, instruction=0, entry=2, left_next=47, right_next=0),
        Register(number=49, instruction=2, entry=2, left_next=92, right_next=50),
        Register(number=50, instruction=1, entry=1, left_next=51, right_next=119),
        Register(number=51, instruction=1, entry=0, left_next=51, right_next=52),
        Register(number=52, instruction=1, entry=1, left_next=52, right_next=53),
        Register(number=53, instruction=1, entry=2, left_next=54, right_next=55),
        Register(number=54, instruction=0, entry=1, left_next=53, right_next=0),
        Register(number=55, instruction=2, entry=1, left_next=84, right_next=56),
        Register(number=56, instruction=1, entry=0, left_next=57, right_next=58),
        Register(number=57, instruction=0, entry=2, left_next=56, right_next=0),
        Register(number=58, instruction=2, entry=1, left_next=84, right_next=59),
        Register(number=59, instruction=1, entry=1, left_next=60, right_next=61),
        Register(number=60, instruction=0, entry=0, left_next=59, right_next=0),
        Register(number=61, instruction=1, entry=2, left_next=62, right_next=63),
        Register(number=62, instruction=0, entry=0, left_next=61, right_next=0),
        Register(number=63, instruction=0, entry=0, left_next=119, right_next=0),
        Register(number=64, instruction=2, entry=1, left_next=84, right_next=65),
        Register(number=65, instruction=1, entry=3, left_next=65, right_next=66),
        Register(number=66, instruction=1, entry=0, left_next=67, right_next=68),
        Register(number=67, instruction=0, entry=3, left_next=66, right_next=0),
        Register(number=68, instruction=1, entry=3, left_next=69, right_next=119),
        Register(number=69, instruction=0, entry=0, left_next=70, right_next=0),
        Register(number=70, instruction=1, entry=3, left_next=71, right_next=119),
        Register(number=71, instruction=1, entry=1, left_next=72, right_next=119),
        Register(number=72, instruction=2, entry=1, left_next=64, right_next=73),
        Register(number=73, instruction=1, entry=4, left_next=73, right_next=74),
        Register(number=74, instruction=1, entry=0, left_next=75, right_next=76),
        Register(number=75, instruction=0, entry=4, left_next=74, right_next=0),
        Register(number=76, instruction=1, entry=1, left_next=77, right_next=119),
        Register(number=77, instruction=2, entry=1, left_next=64, right_next=78),
        Register(number=78, instruction=1, entry=0, left_next=79, right_next=80),
        Register(number=79, instruction=0, entry=4, left_next=78, right_next=0),
        Register(number=80, instruction=1, entry=1, left_next=80, right_next=81),
        Register(number=81, instruction=1, entry=4, left_next=82, right_next=83),
        Register(number=82, instruction=0, entry=1, left_next=81, right_next=0),
        Register(number=83, instruction=2, entry=1, left_next=99, right_next=119),
        Register(number=84, instruction=1, entry=0, left_next=84, right_next=85),
        Register(number=85, instruction=1, entry=1, left_next=86, right_next=119),
        Register(number=86, instruction=0, entry=0, left_next=85, right_next=0),
        Register(number=87, instruction=1, entry=0, left_next=87, right_next=88),
        Register(number=88, instruction=1, entry=1, left_next=89, right_next=90),
        Register(number=89, instruction=0, entry=0, left_next=88, right_next=0),
        Register(number=90, instruction=1, entry=2, left_next=91, right_next=119),
        Register(number=91, instruction=0, entry=0, left_next=90, right_next=0),
        Register(number=92, instruction=1, entry=0, left_next=92, right_next=93),
        Register(number=93, instruction=1, entry=1, left_next=93, right_next=94),
        Register(number=94, instruction=1, entry=2, left_next=95, right_next=119),
        Register(number=95, instruction=1, entry=2, left_next=96, right_next=98),
        Register(number=96, instruction=0, entry=0, left_next=97, right_next=0),
        Register(number=97, instruction=1, entry=25, left_next=0, right_next=94),
        Register(number=98, instruction=0, entry=1, left_next=119, right_next=0),
        Register(number=99, instruction=2, entry=1, left_next=108, right_next=100),
        Register(number=100, instruction=1, entry=0, left_next=101, right_next=103),
        Register(number=101, instruction=1, entry=1, left_next=102, right_next=119),
        Register(number=102, instruction=0, entry=0, left_next=101, right_next=0),
        Register(number=103, instruction=2, entry=1, left_next=113, right_next=104),
        Register(number=104, instruction=1, entry=1, left_next=104, right_next=105),
        Register(number=105, instruction=1, entry=0, left_next=106, right_next=107),
        Register(number=106, instruction=0, entry=1, left_next=105, right_next=0),
        Register(number=107, instruction=1, entry=25, left_next=0, right_next=99),
        Register(number=108, instruction=1, entry=0, left_next=108, right_next=109),
        Register(number=109, instruction=1, entry=2, left_next=110, right_next=119),
        Register(number=110, instruction=1, entry=1, left_next=111, right_next=112),
        Register(number=111, instruction=1, entry=25, left_next=0, right_next=108),
        Register(number=112, instruction=0, entry=0, left_next=119, right_next=0),
        Register(number=113, instruction=1, entry=2, left_next=114, right_next=116),
        Register(number=114, instruction=1, entry=1, left_next=115, right_next=119),
        Register(number=115, instruction=1, entry=25, left_next=0, right_next=113),
        Register(number=116, instruction=1, entry=0, left_next=116, right_next=117),
        Register(number=117, instruction=1, entry=1, left_next=118, right_next=119),
        Register(number=118, instruction=0, entry=0, left_next=117, right_next=0),
    )

    print(process_registers(
        registers=registers,
        index=0,
        table=new_table(int(sys.argv[1])),
    ))
