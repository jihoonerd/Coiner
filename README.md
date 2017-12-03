# Coiner

Auto Cryptocurrency Trading System

* This API-based system is tested in South Korea only.

# Dependencies
* Python 3.6
* Numpy
* Pandas
* Matplotlib

# Setup
1. Clone this repository
```bash
$ git clone https://github.com/jihoon1990/Coiner.git
```

2. Install Packages
* For `pip install`
```bash
$ pip install urllib pandas
```
* For `conda`
```bash
$ conda install urllib pandas
```

2. Create `account_info.py` with `api_key` and `api_secret`
```python
api_key = "YOUR API KEY"
api_secret = "YOUR API SECRET KEY"
```
**Please be careful of exposing your api keys!**


# Updates
Currently, it supports basic fatures only

1. Bid/Ask Order
2. Trade with market price
3. Query orderbook
4. Record the price of cryptocurrency
5. Record the history of trading
3. Bollinger Band

<img src="https://github.com/jihoon1990/Coiner/blob/master/log/2017-10-07%2022:34:36.png?raw=true" width="50%" height="50%">

# Disclaimer
In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, shall any Contributor be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this License or out of the use or inability to use the Work (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses), even if such Contributor has been advised of the possibility of such damages.

# API Source
* Bithumb RESTFul API
