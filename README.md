# DES-SD-AI-SupplyChainData
This repository presents a framework for Resilient Manufacturing Supply Chain Management that integrates Hybrid Simulation (DES-SD) with AI-driven adaptive optimization using Reinforcement Learning (RL) and Evolutionary Algorithms (EAs).

For evaluation, the framework leverages a real-world mobile sales dataset, which includes transactional timestamps, product identifiers, sales quantities, and customer regions. These variables reflect realistic supply chain flows and enable researchers and practitioners to simulate operational events, analyze inventory behavior, and validate optimization policies within a Hybrid Data-Driven Decision Support System.

DataSet can be found from here: https://www.kaggle.com/datasets/vinothkannaece/mobiles-and-laptop-sales-data

Discrete-Event Simulation: The DES model captures short-term inventory dynamics using event-driven logic. It processes daily demand against available stock, applies a reorder policy based on reorder point, reorder quantity, and lead time, and records stockouts when demand exceeds supply. Performance is evaluated through key indicators such as service level, stockouts, and average inventory, making DES suitable for analyzing immediate operational outcomes.

System Dynamics: The SD model represents long-term policy adjustments by modeling aggregate demand variability, lead times, and inventory flows. It dynamically adapts safety stock levels and reorder points using rolling demand volatility and averages, ensuring resilience against fluctuations. This approach emphasizes broader planning horizons and strategic inventory policies rather than event-level execution.

Integrated DES-SD: The hybrid model connects operational execution with policy feedback through bidirectional interaction. DES simulates short-term demand fulfillment and stock movements, while SD updates reorder points and safety stock based on demand volatility and lead time trends. Feedback loops between the two layers enable adaptive control, ensuring that short-term outcomes refine long-term strategies and vice versa.

Reinforcement Learning: The RL module frames inventory control as a Markov Decision Process (MDP), where an agent learns ordering strategies by interacting with the hybrid DES-SD environment. At each step, the agent observes system states (inventory levels, past demand, product attributes, etc) and selects actions such as placing orders. A reward function penalizes stockouts and excess inventory while reinforcing efficient policies, allowing the agent to gradually converge toward adaptive reorder strategies that improve supply chain responsiveness.

Evolutionary Algorithms: The EA module is based on NSGA-II, it optimizes inventory policies by balancing multiple objectives such as minimizing costs and maximizing service levels. Candidate solutions encode parameters like reorder points and safety stock factors, which are evaluated via the DES-SD simulation. Using genetic operators for selection, crossover, and mutation, NSGA-II evolves a diverse population toward the Pareto-optimal frontier, providing decision-makers with optimized trade-offs tailored to strategic priorities.

<img width="1920" height="967" alt="Discrete-Event Simulation" src="https://github.com/user-attachments/assets/026c8567-94da-4f69-9293-e5db6afc5960" />
                            DES Simulation: Inventory Behavior vs. Demand

<img width="1920" height="967" alt="System Dynamics" src="https://github.com/user-attachments/assets/7a26c6f9-a684-450e-aec3-21212db45101" />
                            SD Layer: Demand Volatility and Reorder Point Policy
                            
<img width="1920" height="967" alt="Integrated DES-SD Model" src="https://github.com/user-attachments/assets/a47cc864-2d84-4e7a-a280-dec5fa53ebd9" />
                            DES Execution Enhanced with SD-Driven Policy Updates

<img width="1920" height="967" alt="Integrated DES-SD-AI Models" src="https://github.com/user-attachments/assets/81a5f518-a2d3-410b-9dbd-eb06c2873ff4" />
                            AI-Enhanced Inventory Optimization: DES + SD + RL + EA
