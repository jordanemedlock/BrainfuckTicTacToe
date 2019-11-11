try:
  from brainfuck import Brainfuck
  from metabf import *
except:
  pass
  

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
  