# Monte Carlo Life Insurance Pricing Model

This project implements a stochastic simulation to price a **Term Life Insurance** policy. Unlike deterministic models, this uses Monte Carlo methods to simulate thousands of individual life paths based on mortality probabilities.

## 🛠 Features
- **Vectorized Simulation:** Uses NumPy for high-performance modeling of 100,000+ policyholders.
- **Actuarial Logic:** Incorporates survival probabilities ($p_x$) and death probabilities ($q_x$) using a Gompertz-Makeham distribution.
- **Financial Discounting:** Calculates the Net Single Premium (NSP) by discounting future death benefits to their Present Value (PV).
- **Risk Loading:** Includes an expense loading factor to simulate commercial pricing.

## 📈 Methodology
The model follows the fundamental actuarial equation for a term insurance benefit:

$$A^1_{x:n|} = \sum_{t=0}^{n-1} v^{t+1} \cdot {}_t|q_x$$

Where:
- $v$ is the discount factor $1/(1+i)$
- ${}_t|q_x$ is the probability of a person aged $x$ dying in year $t$.

