def interact(ns):
     try:
          from IPython import embed
     except ImportError:
          import code
          code.interact(local=ns)
     else:
          embed(user_ns=ns)
