<p align="center"><img src="https://github.com/nathanbronson/StochasticBaskets/blob/main/logo.jpg?raw=true" alt="logo" width="200"/></p>

_____
# StochasticBaskets
predicting and seeding the NCAA Tournament with stochastic models

## About
StochasticBaskets is a project that predicts and seeds the NCAA Tournament with stochastic models. StochasticBaskets builds on [BasketWise](https://github.com/nathanbronson/BasketWise), a previous experiment in predicting the NCAA Tournament outcomes using machine learning. StochasticBaskets was built by Nathan Bronson, Edward Donson, Tyler Headley, and Matthew Shield.

We use a random forest classifier to assign probabilities to each possible outcome of a tournament game based on each team's statistics. We then use simulated annealing to find the most likely tournament outcome based on this model. We also use the Metropolis-Hastings algorithm to sample from the set of tournament outcomes according to likelihood. From samples generated in this way, we compute various metrics that measure the robustness of the tournament's seeding. We then use basin hopping to find the optimal seeding according to these metrics.

To evaluate our methods, we use data from the 2023 NCAA Tournament. We evaluate our outcome prediction model, finding that our methods converge on an outcome six times more likely than the output of a naive, greedy benchmark. We evaluate our seeding model, finding that our method outperforms a naive baseline in terms of predictive power against its most likely outcome and performs just as well at predicting the actual tournament outcome. Our seeding model’s performance is even more remarkable against the NCAA’s official seedings, which it significantly outperforms in explaining both its most likely outcome and the real tournament outcome.

## Usage
The various experiments the project investigates are implemented in `main.py`. These projects rely on matchup probability models created by executing `prob.py`. Visualizations and analysis from the report along with the code to generate them can be found in the following notebooks: `graphs.ipynb`, `naive_approaches.ipynb`, and `prob_model_desc.ipynb`.

## License
See `LICENSE`.

## Report

![page1](./images/report%20page%201.png)
![page2](./images/report%20page%202.png)
![page3](./images/report%20page%203.png)
![page4](./images/report%20page%204.png)
![page5](./images/report%20page%205.png)
![page6](./images/report%20page%206.png)
![page7](./images/report%20page%207.png)
![page8](./images/report%20page%208.png)
![page9](./images/report%20page%209.png)
![page10](./images/report%20page%2010.png)
![page11](./images/report%20page%2011.png)
![page12](./images/report%20page%2012.png)
![page13](./images/report%20page%2013.png)
![page14](./images/report%20page%2014.png)
![page15](./images/report%20page%2015.png)
![page16](./images/report%20page%2016.png)
![page17](./images/report%20page%2017.png)
