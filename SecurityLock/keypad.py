# Copyright (c) 2024 Tim Collins - MIT License
# See https://github.com/drtimcollins/6E5Z0027-Embedded-Systems/blob/main/LICENSE

from machine import Pin, Timer

class Keypad():
    _keyValues = ("123A","456B","789C","*0#D")
    def __init__(self,*,rows,columns,callback):
        self._rowPins = rows
        self._colPins = columns
        self._keyStates = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
        self._keyPressed = callback
        for p in rows:
            p.init(Pin.IN, Pin.PULL_UP)
        for p in columns:
            p.init(Pin.OPEN_DRAIN, value = 1)
        self._tmr = Timer(freq = 100, callback=self._scanKeys)

    def _scanKeys(self, timer):
        for col in range(4):                                      # Scan through all 4 columns
            self._colPins[col].value(0)                           # Connects the column to GND
            for row in range(4):                                  # Scan through all 4 rows
                if self._rowPins[row].value() != self._keyStates[row][col]:
                    self._keyStates[row][col] = self._rowPins[row].value()
                    if self._keyStates[row][col] == 0:            # Respond if new state is 0,
                        self._keyPressed(Keypad._keyValues[row][col])
            self._colPins[col].value(1)                           # Set column to 'floating'
