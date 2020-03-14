#!/usr/bin/env python3

"""
https://stackoverflow.com/questions/60510955/how-to-store-x-number-of-factors-from-user-input-gtk-textview-in-multi-factor
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys
import operator


class Handlers:
    def __init__(self):
        print('__init__:()'.format())
        self.expressionField = builder.get_object("expressionField")
        self.buffer = self.expressionField.get_buffer()
        self.buffer.insert(self.end_iter, '5x5 + 2 / 3÷2+ 10 % - 1')

    @property
    def end_iter(self):
        return self.buffer.get_end_iter()

    @property
    def start_iter(self):
        return self.buffer.get_start_iter()

    def clear(self):
        self.buffer.delete(self.start_iter, self.end_iter)

    def on_clicked(self, button, data=None):
        label = button.get_label()
        print('clicked:{}'.format(label))
        
        if label == 'Clear':
            self.clear()
            return
        
        elif label == '=':
            # do validation and eval
            text1 = self.buffer.get_text(self.start_iter, self.end_iter, False)
            
            # Replace with Python syntax
            text1 = text1.replace('x', '*')
            
            # Evaluate the expression
            try:
                # text = str(eval(text1))
                text = str(self.eval(text1))
            except (ValueError, SyntaxError) as e:
                text = str(e)
            finally:
                print('\tbuffer:{}'.format((text1, text)))
                
            self.clear()
        else:
            text = label
            
        self.buffer.insert_at_cursor(text)
        
    def eval(self, expr):
        import re
        import math
        
        def mul(v, f):
            return v * f
        
        def add(v1, v2):
            return v1 + v2
        
        def div(v, d):
            return v / d
        
        def sub(v1, v2):
            return v1 -v2
        
        # 5x5 + 2 / 3÷2+ 10 % - 1
        # [('5', '', '', ''), ('*5', '*', '5', ''), ('+ 2', '+', '2', ''), ('/ 3', '/', '3', ''), 
        # ('÷2', '÷', '2', ''), ('+ 10 %', '+', '10', ' %'), ('- 1', '-', '1', '')]
        e = re.findall('(\d+|([+-x*/÷]?)\s?(\d+)(\s%|%)?)', expr)        
        # print('\te:{}'.format(e))
        
        r = None
        for v in e:
            op = {'*': mul, 'x': mul, '+': add, '/': div, '÷': div, '-': sub}.get(v[1], None)
            if op is not None and not v[3]:
                r = op(r, float(v[2]))
                
            elif op is not None and '%' in v[3]:
                # print('v%:{}'.format(v))
                r = mul(r, (float(v[2]) / 100))
                
            else:
                r = float(v[0])
                
            # print('\tr:{}'.format(r))
        return r

    def on_main_Window_destroy(self, *args, data=None):
        Gtk.main_quit()

    def on_invalidExpressionButton_clicked(self, button, data=None):
        invalid_Expression_Dialog = builder.get_object(
            "invalid_Expression_Dialog")
        invalid_Expression_Dialog.hide()
        
        self.clear()


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.add_from_file("SimpleCalculator2.glade")
    builder.connect_signals(Handlers())
    
    main_Window = builder.get_object("main_Window")
    main_Window.show()
    
    Gtk.main()
