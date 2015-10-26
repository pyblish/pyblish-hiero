"""
Puts the active selection into 'hiero.selection'
"""

import hiero

def selectionChanged(event):
    hiero.selection = event.sender.selection()

hiero.core.events.registerInterest('kSelectionChanged', selectionChanged)
