try:
  from brainfuck import Brainfuck
except:
  pass
  
def move(start, end):
  n = end - start
  absn = abs(n)
  s = absn*'>' if n >= 0 else absn*'<'
  return f"""{s}{absn}"""

# all values are relative to initial location
# assumes dest and temp are 0
def cp(src, dest, temp): # dest = src
  return f"""
    (cp {src} {dest} {temp}
      {move(0, src)} [
        {move(src, temp)} + {move(temp, dest)} + {move(dest, src)} - 
      ]
      {move(src, temp)} [
        {move(temp, src)} + {move(src, temp)} -
      ]
      {move(temp, 0)}
    )
  """

def zero(loc): # loc = 0
  return f'Z{move(0,loc)}[-]{move(loc,0)}Z '

def const(loc, value): # loc = value
  return f'C{move(0, loc)} {zero(0)} {"+"*value}C '

def add(dest, src, temp): # dest = dest + src
  return f"""
    (add {dest} {src} {temp}
      {zero(temp)}
      {move(0, src)} [
        {move(src, dest)} + {move(dest, temp)} + {move(temp, src)} -  
      ]
      {move(src, temp)} [
        {move(temp, src)} + {move(src, temp)} -
      ]
      {move(temp, 0)}
    )
  """

def sub(dest, src, temp): # dest = dest - src
  return f"""
    (sub {dest} {src} {temp}
      {zero(temp)}
      {move(0, src)} [
        {move(src, dest)} - {move(dest, temp)} + {move(temp, src)} - 
      ]
      {move(src, temp)} [
        {move(temp, src)} + {move(src, temp)} - 
      ]
      {move(temp, 0)}
    )
  """

def mult(dest, src, temp1, temp2): # dest = dest * src
  return f"""
    (mult {dest} {src} {temp1} {temp2}
      {zero(temp1)} {zero(temp2)} # zero out our temps
      {move(0, dest)} [       # move dest to temp2
        {move(dest, temp2)} + 
        {move(temp2, dest)} - 
      ]
      {move(dest, temp2)} [   # foreach temp2
        {move(temp2, src)} [  # add src to dest and move to temp1
          {move(src, temp1)} + 
          {move(temp1, dest)} + 
          {move(dest, src)} - 
        ]
        {move(src, temp1)} [  # move temp1 back to src
          {move(temp1, src)} + 
          {move(src, temp1)} - 
        ]
        {move(temp1, temp2)} -  # remove one from dest
      ]
    )
  """


def if_else(cond, true, false, temp0, temp1): # if (cond != 0) {true} else {false}
  return f"""
    (if_else {cond} true false {temp0} {temp1}
      {zero(temp0)}{zero(temp1)}
      {cp(cond, temp1, temp0)}
      {move(0, temp0)} + 
      {move(temp0, temp1)} [
        (true
          {true}
        )
        {move(temp1, temp0)} - 
        {move(temp0, temp1)} [-]
      ]
      {move(temp1, temp0)} [
        (false
          {false}
        )
        -                      
      ]
      {move(temp0, 0)} 
    )
  """

# temp0 only needs to contain 0
# it is zeroed out and used to stop a loop
def if_true(cond, true, temp0): # if (cond) {true}
  return f"""
    (if_true true {temp0}
      {zero(temp0)}
      {move(0, cond)} [
        (true
          {true}
        )
        {move(cond, temp0)}
      ]
      {move(cond, 0)}
    )
  """

def logical_not(cond, temp):
  return f"""
    (logical_not {cond} {temp}
      {zero(temp)}
      {move(0,cond)} [                              
        {move(cond, temp)} + {move(temp, cond)} [-] 
      ] +                                           
      {move(cond, temp)} [                          
        {move(temp, cond)} - {move(cond, temp)} -   
      ]
      {move(temp, 0)}
    )
  """

# destroys cond
def if_false(cond, false, temp): # if (cond == 0) {false}
  return f"""
    (if_false {cond} false {temp}
      {logical_not(cond, temp)}
      {if_true(cond, false, temp)}
    )
  """

def validate_row(row, ret, temp0, temp1, temp2, temp3):
  x0 = row * 3
  x1 = row * 3 + 1
  x2 = row * 3 + 2

  return f"""
    (validate_row {row} {ret} {temp0} {temp1} {temp2} {temp3}
      {move(0,temp0)}[-]{move(temp0,temp1)}[-]{move(temp1,temp2)}[-]{move(temp2,temp3)}[-]{move(temp3,ret)}[-] # zero all these
      {cp(x0, temp0, temp1)}
      {sub(temp0, x1, temp1)}
      {cp(x1, temp1, temp2)}
      {sub(temp1, x2, temp2)}
      {
        if_false(temp0, 
          if_false(temp1,
            cp(x0, ret, temp3),
          temp2),
        temp2)
      }
    )
  """
  
temp0 = 9
temp1 = 10

program = validate_row(0, 9, 10, 11, 12, 13)

# program = """
# [>>>>>>>>>>>+<+<<<<<<<<<<-] # move 0 into temp0 and temp1
# <[<<<<<<<<<<+>>>>>>>>>-] # move temp0 back into 0

# """

# program = '['+m(9)+'+'+m(1)+'+'+m(-10)+'-'+']'
# program += m(9)+'['+m(-9)+'+'+m()

# program = f'[{move(9)}+{move(1)}+{move(-10)}-]'
# program += f'{move(9)}[{move(-9)}+{move(9)}-]'

print(program)

# 0 is empty
# 1 is X
# 2 is O
tape = [
  1,2,0, # first row
  0,0,0, # second row
  0,0,0, # third row
  0, # temp0: 9
  0, # temp1: 10
  0,  # temp2: 11
  0,
  0,
  0,
  0,
  0
]

Brainfuck(tape, 0, verbose=True, wait_time=0.5).run(program)