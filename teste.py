import pandas as pd

impressoras = {'printers': ['impressora1', 'impressora2']}
df = pd.DataFrame(impressoras)
log = '\n'
log = log.join(df.printers)

print(log)