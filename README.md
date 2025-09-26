# DES-SD-AI-SupplyChainData
This repository presents a framework for Resilient Manufacturing Supply Chain Management that integrates Hybrid Simulation (DES-SD) with AI-driven adaptive optimization using Reinforcement Learning (RL) and Evolutionary Algorithms (EAs).

For evaluation, the framework leverages a real-world mobile sales dataset, which includes transactional timestamps, product identifiers, sales quantities, and customer regions. These variables reflect realistic supply chain flows and enable researchers and practitioners to simulate operational events, analyze inventory behavior, and validate optimization policies within a Hybrid Data-Driven Decision Support System.

DataSet can be found from here: https://www.kaggle.com/datasets/vinothkannaece/mobiles-and-laptop-sales-data

Discrete-Event Simulation: The DES model captures short-term inventory dynamics using event-driven logic. It processes daily demand against available stock, applies a reorder policy based on reorder point, reorder quantity, and lead time, and records stockouts when demand exceeds supply. Performance is evaluated through key indicators such as service level, stockouts, and average inventory, making DES suitable for analyzing immediate operational outcomes.

System Dynamics: The SD model represents long-term policy adjustments by modeling aggregate demand variability, lead times, and inventory flows. It dynamically adapts safety stock levels and reorder points using rolling demand volatility and averages, ensuring resilience against fluctuations. This approach emphasizes broader planning horizons and strategic inventory policies rather than event-level execution.

Integrated DES-SD: The hybrid model connects operational execution with policy feedback through bidirectional interaction. DES simulates short-term demand fulfillment and stock movements, while SD updates reorder points and safety stock based on demand volatility and lead time trends. Feedback loops between the two layers enable adaptive control, ensuring that short-term outcomes refine long-term strategies and vice versa.

Reinforcement Learning: The RL module frames inventory control as a Markov Decision Process (MDP), where an agent learns ordering strategies by interacting with the hybrid DES-SD environment. At each step, the agent observes system states (inventory levels, past demand, product attributes, etc) and selects actions such as placing orders. A reward function penalizes stockouts and excess inventory while reinforcing efficient policies, allowing the agent to gradually converge toward adaptive reorder strategies that improve supply chain responsiveness.

Evolutionary Algorithms: The EA module is based on NSGA-II, it optimizes inventory policies by balancing multiple objectives such as minimizing costs and maximizing service levels. Candidate solutions encode parameters like reorder points and safety stock factors, which are evaluated via the DES-SD simulation. Using genetic operators for selection, crossover, and mutation, NSGA-II evolves a diverse population toward the Pareto-optimal frontier, providing decision-makers with optimized trade-offs tailored to strategic priorities.
                            
