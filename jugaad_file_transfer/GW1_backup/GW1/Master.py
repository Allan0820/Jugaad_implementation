import numpy as np 
from NetHealthMonitor import *
from ResetTheNetwork import *

Subnet_status = Get_Subnet_Health()

print Subnet_status

Reset_Subnet()