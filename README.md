# Coiner

Auto Cryptocurrency Trading System

# Introduction
암호화폐를 프로그래밍을 통해 프로그램매매를 할 수 있습니다.

# Dependencies

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
3. 볼린저 밴드

# Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# API Source
* Bithumb RESTFul API