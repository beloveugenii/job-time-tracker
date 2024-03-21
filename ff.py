#!/usr/bin/env python3
import datetime

d = datetime.date.today()
td = datetime.timedelta(31)

actions = { 'q': lambda: exit(0),
            'p': lambda: print((d-td).isoformat()),
            'n': lambda: print((d+td).isoformat()),
           }


actions[input()]()

