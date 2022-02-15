def secondsToText(unit, granularity = 2):

  ratios = {
    'decades' : 311040000, # 60 * 60 * 24 * 30 * 12 * 10
    'years'   : 31104000,  # 60 * 60 * 24 * 30 * 12
    'months'  : 2592000,   # 60 * 60 * 24 * 30
    'days'    : 86400,     # 60 * 60 * 24
    'hours'   : 3600,      # 60 * 60
    'minutes' : 60,        # 60
    'seconds' : 1          # 1
  }

  texts = []
  for ratio in ratios:
    result, unit = divmod(unit, ratios[ratio])
    if result:
      if result == 1:
        ratio = ratio.rstrip('s')
      texts.append(f'{result} {ratio}')
  texts = texts[:granularity] 
  if not texts:
    return f'0 {list(ratios)[-1]}'
  text = ', '.join(texts)
  if len(texts) > 1:
    index = text.rfind(',')
    text = f'{text[:index]} and {text[index + 1:]}'
  return text


print(secondsToText(99999933333))