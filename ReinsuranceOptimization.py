'''
Reinsurance Optimization
+++++++++++++++++++++++++++++++++++

Once upon a time, in the peaceful town of Insureville, there was a small insurance company called SafeGuard Insurance. SafeGuard 
Insurance provided coverage to the residents of Insureville, protecting them from various risks such as property damage, accidents, 
and natural disasters.

As the business grew, the management of SafeGuard Insurance realized that they needed to manage their own risk exposure more 
effectively. They decided to explore the world of reinsurance, where they could transfer some of their risks to other companies, 
called reinsurers.

In their quest to find the best reinsurance options, SafeGuard Insurance discovered that there were three different reinsurance 
layers available in the market, each offered by a different reinsurer. Each layer had its own price tag, coverage limit, and retention 
level.

The first layer, offered by Reinsurer A, cost $1,000 and provided coverage up to $50,000. SafeGuard Insurance would retain no risk for 
this layer. Reinsurer A had a strong credit rating, indicating a low probability of default.

The second layer, offered by Reinsurer B, cost $2,000 and provided coverage up to $100,000. For this layer, SafeGuard Insurance would 
retain $50,000 of risk. Reinsurer B had a slightly lower credit rating than Reinsurer A, indicating a slightly higher probability of 
default.

The third layer, offered by Reinsurer C, cost $3,000 and provided coverage up to $150,000. SafeGuard Insurance would retain $150,000 of 
risk for this layer. Reinsurer C had the lowest credit rating among the three reinsurers, indicating a higher probability of default.

SafeGuard Insurance wanted to transfer a total of $180,000 worth of risk to reinsurers while minimizing their costs. They also wanted to
ensure that they purchased reinsurance from at least two different reinsurers to diversify their risk and reduce their reliance on any 
single reinsurer.

To find the best combination of reinsurance layers, SafeGuard Insurance used a magical tool called the Reinsurance Optimizer. The 
Reinsurance Optimizer considered the costs, coverage limits, retentions, and credit ratings of each reinsurance layer, as well as the 
target risk transfer and diversification requirements.

After running the Reinsurance Optimizer, SafeGuard Insurance discovered the optimal solution: they should purchase the first layer from 
Reinsurer A and the second layer from Reinsurer B. This combination would allow them to transfer the desired amount of risk while 
minimizing their costs and maintaining diversification.

With the help of the Reinsurance Optimizer, SafeGuard Insurance was able to make an informed decision and secure the best reinsurance 
coverage for their needs. The residents of Insureville continued to enjoy the protection provided by SafeGuard Insurance, knowing that 
their beloved insurance company was well-prepared to handle any risks that came their way. And they all lived happily ever after.

'''

import dimod
from dwave.system import LeapHybridCQMSampler

# Data  
num_layers = 3  
reinsurance_costs = [1000, 2000, 3000]  # Cost of each reinsurance layer  
reinsurance_limits = [50000, 100000, 150000]  # Limit of each reinsurance layer  
reinsurance_retentions = [0, 50000, 150000]  # Retention of each reinsurance layer  
reinsurer_credit_ratings = [0.95, 0.90, 0.85]  # Credit rating of each reinsurer (1 - probability of default)  
target_risk_transfer = 180000  # Target amount of risk to transfer  
min_reinsurers = 2  # Minimum number of different reinsurers for diversification 

# Devided by 1000 to create smaller solution space
# Data  
num_layers = 3  
reinsurance_costs = [1, 2, 3]  # Cost of each reinsurance layer  
reinsurance_limits = [50, 100, 150]  # Limit of each reinsurance layer  
reinsurance_retentions = [0, 50, 150]  # Retention of each reinsurance layer  
reinsurer_credit_ratings = [0.95, 0.90, 0.85]  # Credit rating of each reinsurer (1 - probability of default)  
target_risk_transfer = 180  # Target amount of risk to transfer  
min_reinsurers = 2 

# Create binary variables y[i] representing whether reinsurance layer i is purchased  
y = {}  
for i in range(num_layers):  
    y[i] = dimod.Binary(f'y[{i}]')

cqm = dimod.ConstrainedQuadraticModel()

# Create constraints to ensure the target risk transfer is achieved  
cqm.add_constraint(sum([y[i] * reinsurance_limits[i] for i in range(num_layers)]) >= target_risk_transfer )

# Create constraints to ensure diversification  
cqm.add_constraint(sum([y[i] for i in range(num_layers)]) >= min_reinsurers)

# Define the objective function: minimize the total cost of reinsurance, adjusted for counterparty risk  
objective = sum([reinsurance_costs[i] * y[i] / reinsurer_credit_ratings[i] for i in range(num_layers)])  
cqm.set_objective(objective)

DWAVE_API_TOKEN = "DEV-*******" # Add your D-wave API Token

sampler = LeapHybridCQMSampler(token = DWAVE_API_TOKEN)

sampleset = sampler.sample_cqm(cqm,time_limit=180,label="Reinsurance Optimization")

best = sampleset.first

print(f'Minimum total reinsurance cost (adjusted for counterparty risk): {best.energy*1000}')

output_layers = best.sample
selected_layers = []
for x, y in output_layers.items():
    if y > 0:
        selected_layers.append(x)
print(f'Optimal reinsurance layers to purchase: {selected_layers}') 

