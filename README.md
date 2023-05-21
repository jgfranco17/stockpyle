<h1 align="center">Stockpyle: An Algorithmic Trading Bot</h1>

<div align="center">

![STATUS](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)
![LICENSE](https://img.shields.io/badge/license-BSD3Clause-blue?style=for-the-badge)

</div>

---

## 📝 Table of Contents

* [About](#about)
* [Getting Started](#getting_started)
* [Usage](#usage)
* [Testing](#testing)
* [Authors](#authors)

## 🔎 About <a name = "about"></a>

Stockpyle is a Python-based trading bot that leverages algorithmic strategies to automate trading activities in financial markets.

### Background

Algorithmic trading has gained significant popularity in financial markets due to its potential to automate trading decisions, increase efficiency, and exploit market opportunities. By leveraging advanced data analysis and execution algorithms, algorithmic trading bots can execute trades with precision and speed, allowing traders to capitalize on market movements in a timely manner.

Stockpyle aims to provide a comprehensive solution for developing and deploying algorithmic trading bots using Python. It combines expertise in Python programming and financial markets to empower users to design, code, backtest, and optimize their own algorithmic trading strategies.

### Motivation

Stockpyle aims to combine the powers of software engineering and financial analysis in order to enhance algorithmic trading.

The key motivations for building this algorithmic trading bot framework are:

1. **Efficiency and Speed**: Manual trading is limited by human capabilities and can be prone to delays and emotions. Algorithmic trading allows for rapid execution and removes emotional biases, enabling traders to take advantage of fleeting market opportunities.

2. **Backtesting and Optimization**: By providing tools for backtesting trading strategies using historical data, traders can evaluate the performance of their algorithms under various market conditions. This helps in identifying and optimizing strategies that have the potential for consistent profitability.

3. **Risk Management**: Implementing risk management techniques is crucial to protect capital and manage potential losses. Stockpyle emphasizes incorporating risk management functionalities, such as position sizing and stop-loss orders, into the algorithmic trading bots to ensure responsible and prudent trading practices.

---

**Note:** Algorithmic trading involves financial risks, and users are responsible for understanding and managing these risks. It's essential to conduct thorough testing, validate strategies, and adhere to legal and ethical considerations while deploying trading bots in live trading environments.

---


## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before running Stockpyle, make sure you have the following prerequisites installed:

* [Python 3.9](https://github.com/pyenv/pyenv) or above
* pip package manager

Stockpyle is being developed on Ubuntu 22.04, but should work on MacOS or other Linux distros.

### Creating a Virtual Environment

It is recommended to create a [virtual environment](https://docs.python.org/3/library/venv.html). This will ensure that the working environment has all the necessary dependencies installed without conflicting with the base interpreter.

```bash
# Create a virtual environment named "venv"
python3 -m venv venv
source venv/bin/activate
```

### Installing

To get started with Stockpyle, clone the repository to your local machine and install the required dependencies.

```bash
git clone https://github.com/jgfranco17/stockpyle.git
cd stockpyle
pip install -r requirements.txt
```

## 🚀 Usage <a name = "usage"></a>

As the project progresses, usage instructions will be provided here.

### CLI usage

To run the bot, simply execute either of the following commands. If you choose to use the Makefile option, remember to set your preference of stock symbol in the top variables.

```bash
# Use the prebuilt Makefile
make run

# Specify your own configuration
python3 app.py <stock symbol>
```

If you wish to export the trading logs as a JSON file, add in the optional `--export-data` flag.

```bash
python3 app.py <stock symbol> --export-data
```

## 🔧 Testing <a name = "testing"></a>

In order to run diagnostics and unittests, install the testing dependencies found in the `requirements-test.txt` file. This will allow you to utilize the full capacity of the test modules we have built.

To run the full test suite, run the Makefile command as follows:

```bash
make test
```

This will run the test module and generates a detailed result report.

### Using PyTest CLI

You can run these tests using the [PyTest](https://docs.pytest.org/en/7.3.x/) CLI. To run all tests in the directory containing the test files, navigate to the directory and enter `pytest` in the command line; for added verbosity, add the `-vv` flag after. To run a specific test file, enter `pytest <filename>`.

```bash
# Run all tests in the testing module with full detail
pytest -vv

# Run a specific test file
cd stockpyle/tests
pytest test_transactions.py
```

### Why these tests are important

Running these unittests is necessary to ensure that the code is functioning as expected and meeting the requirements of the design specification. The unittests are designed to test each function and method of the code and to identify any errors or unexpected behavior. By testing the code using these PyTest unittests, we can ensure that the code meets the specified requirements and that any changes made to the code do not introduce new bugs or errors.

In addition, these tests can be automated to run on every code change, allowing us to quickly identify any issues that may arise and enabling us to maintain a high level of code quality. 

In essence, running these PyTest unittests is a critical part of the software QA process and helps to ensure that our code is robust, reliable, and meets the needs of our end-users before the product hits deployment.

## ✒️ Authors <a name = "authors"></a>

* [Joaquin Franco](https://github.com/jgfranco17) 
