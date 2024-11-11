# Fund2Vec: Mutual Funds Similarity using Graph Learning

This repository implements a Fund2Vec model for determining similarities across Indian equity mutual funds based on asset composition. Using techniques in graph learning, we construct a weighted bipartite graph of funds and their underlying assets, followed by a Node2Vec embedding for structural similarity computation. The cosine similarity and Jaccard index evaluations help quantify similarity between funds based on their asset compositions.

## Research Paper
The methodology in this repository is based on the paper **[Fund2Vec: Mutual Funds Similarity using Graph Learning](https://arxiv.org/pdf/2106.12987)** by Vipul Satone, Dhruv Desai, and Dhagash Mehta. You can find and read the full paper [here](https://arxiv.org/pdf/2106.12987).

## Dataset
To replicate this study, we gathered a dataset of equity funds in India, capturing each fund’s portfolio of assets and the respective weight of each asset. The dataset is stored in a CSV file, `combined_fund_data.csv`, with the following format:

| Fund Name       | Asset A | Asset B | Asset C | ... |
|-----------------|---------|---------|---------|-----|
| Fund1           | 0.2     | 0.3     | 0       | ... |
| Fund2           | 0       | 0.1     | 0.4     | ... |

Each fund is represented as a row, with columns representing the percentage weight of each asset in the portfolio.

## Requirements

Install the required packages with:
```bash
pip install pandas numpy networkx gensim scikit-learn
