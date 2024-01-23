import os
import random
from datetime import datetime
from . import github as gggh
from . import logger as gglg

LG_ID = 0

def run_batch_w_logger(batch_no, lid, ALL_LOGGER):
  global LG_ID
  gglg.ALL_LOGGER = ALL_LOGGER
  gglg.save_log(LG_ID, '=> [B] ' + str(batch_no))
  return ALL_LOGGER
  
