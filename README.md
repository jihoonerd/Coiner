# Coiner

Auto Cryptocurrency Trading System

# Introduction
암호화폐를 프로그래밍을 통해 프로그램매매를 할 수 있습니다.

# Setup
1. Repositroy를 clone합니다.
```bash
git clone https://github.com/jihoon1990/Coiner.git
```
2. Root folder에 account_info.py를 만들고 api_key,와 api_secret을 입력합니다.
```python
api_key = "YOUR API KEY"
api_secret = "YOUR API SECRET KEY"
```
**gitignore에서 account_info.py를 제외하도록 하였습니다. API KEY가 유출되지 않도록 주의하시기 바랍니다.**

3. `Trader` class의 `run_trading` method를 통해 거래를 시작할 수 있습니다.

# Example
다음 command를 통해 demo를 실행할 수 있습니다. ***실제 거래를 발생시키므로 유의하시기 바랍니다.***

```bash
python -i tester.py
```

# Updates
현재 초기 버전으로 기초적인 기능만 지원합니다. 현재 제공되는 주요사항은 다음과 같습니다.

1. 지정가 거래
2. 시장가 거래
3. 내 계좌 업데이트
4. 호가창 조회 (최대 매도, 매수 각 20호가 까지 조회 가능)
5. 시세 기록
3. Bollinger Band

<img src="https://github.com/jihoon1990/Coiner/blob/master/log/2017-10-07%2022:34:36.png?raw=true" width="50%" height="50%">

# Disclaimer
In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, shall any Contributor be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this License or out of the use or inability to use the Work (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses), even if such Contributor has been advised of the possibility of such damages.

# API Source
* Bithumb RESTFul API
