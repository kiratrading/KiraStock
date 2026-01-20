# Naked Long 實戰：時間值 (Theta) 與 爆發力 (Gamma) 的博弈

**Category:** Options Theory | **Level:** Advanced

作為前投行家及活躍交易者，我們明白 **Naked Long (單邊長倉)**，不論是做 CALL 還是 PUT，都是一場「與時間競賽」的遊戲。

在 HSI 27,000 這個水平，要同時「最大化利潤」與「保護倉位」是一個 Trade-off (取捨)。關鍵在於對 **Greeks (希臘字母)** 的掌控，特別是 **Theta (時間值損耗)** 和 **Gamma (價格加速感)** 的博弈。

---

## 劇本一：橫盤為主，突然會有一日大升 (The "Lurking" Play)

**普遍人的盲點：** 買遠 Strike (Deep OTM) + 月權 (Monthly)。這是一個危險的陷阱。

### 問題所在：
1.  **Theta Bleed (時間值失血)：** 在橫盤期間，Theta 會每日割你的肉。如果你買 Deep OTM，你的權利金全是 Time Value (時間值)，一旦橫盤太久，就算最後真的大升，升幅可能只剛好抵銷之前損耗的時間值，導致「看對市，沒賺錢」。
2.  **Delta 低：** 遠 Strike 的 Delta 很低 (例如 0.1 - 0.2)。HSI 升 500 點，你的 Option 可能只升很少，槓桿效應在初期出不來。試想像你的 Call 快到期且接近 Strike，大戶為什麼要讓你平倉？一到 Expiry，就算你幾接近 Strike，都會化 0。

### 優化策略 (Maximize Profit + Protection)：
* **Expiry (到期日)：** 不要買當月 (Front Month)。 **買入 2-3 個月後到期** 的季權或遠月權。這樣可以將 Theta 損耗降到最低 (Longer duration, lower daily theta decay)，這是對抗橫盤的唯一「保護」。
* **Strike (行使價)：** 選擇 **ATM (價平 27000)** 或 **Slightly OTM (輕微價外 27200-27400)**。
* **理由：** ATM 的 Delta 約 0.5，一但大升開始，Gamma 會推動 Delta 迅速接近 1.0，利潤增長最實質。
* **操作心法：** 這種倉位是「用時間換空間」。你在等待波動率 (IV) 的回歸和突破。

---

## 劇本二：明天就大升，Gap Up Open (The "Lotto" Play)

**你的想法：** 買 Weekly ATM / Slight OTM。
**我的點評：** 完全正確，這是狙擊手的打法。

### 獲利邏輯：
你要的是 **Gamma Explosion**。臨近到期的 Weekly Option，Gamma 值最大。這意味著 HSI 每升 1 點，你的 Delta 增加速度最快。如果是 Gap Up，你需要的是能在開市一瞬間價格翻倍的工具。

### Strike 選擇 (進擊 vs 保守)：
1.  **激進型 (Maximize ROI%)：** 買 OTM，例如 27400 - 27600 (Delta ~0.25-0.30)。
    * **理由：** 權利金便宜。如果明天 HSI Gap Up 500 點直穿 27500，這張 Option 會直接從 OTM 變成 ITM，權利金可能翻 3-5 倍。這是以小博大的極致。
2.  **穩健型 (Balance)：** 買 ATM (27000) 或 Slightly ITM (26800)。
    * **理由：** 即使 Gap Up 幅度不如預期 (例如只升 200 點)，ATM 也能立即獲利。OTM 如果沒升穿 Strike，開市 IV 一縮 (IV Crush)，價格可能不升反跌。

![IV Crush 示意圖](Education/images/opt_strike_1.jpg)

---

## 數據回測：橫盤 vs 爆升

### 1. 橫盤 (Scenario 1: Sideways 5 Days)
* **Weekly (本週):** **全軍覆沒**。 ATM (27000) 的 Weekly Call 即使 HSI 價格沒跌，5 天後價值蒸發了 97.8%。OTM (27200+) 直接歸零 (-100%)。這就是為什麼橫盤時買 Weekly 等於自殺。
* **Monthly (遠月):** **輕微擦傷**。 ATM 的 Monthly Call 只損失了約 6.1% 的時間值。這就是為什麼說買遠月是用來「保護倉位」避免被 Theta 磨死。

### 2. 爆升 (Scenario 2: Gap Up +500 Pts Next Day)
* **Weekly (本週):** **以小博大的極致**。 買入 OTM (27600) 的 Weekly Call，雖然一開始是價外，但一天內 ROI 高達 137.3%。注意 Strike 越高，爆發力越強（當然風險也越高）。
* **Monthly (遠月):** **賺錢，但無驚喜**。 ROI 大約在 30% 左右。這裡主要賺的是 Delta (股價升幅)，而非 Gamma (加速度)。

---

## 總結操作矩陣 (Summary Table)

| 預期情境 | 關鍵敵人 | 建議 Expiry | 建議 Strike | 戰術重點 |
| :--- | :--- | :--- | :--- | :--- |
| **橫盤待變 (Scenario 1)** | **Theta (時間)** | 遠月 (60-90日) | ATM / 近 OTM | 買時間保護倉位，避免被盤整磨死。保留實力等大浪。 |
| **明日爆升 (Scenario 2)** | **Delta/Timing** | Weekly (本週) | OTM (Delta ~0.3) | 利用高 Gamma 在短時間內創造最大爆發力。 |

---

## Python 量化驗證 (Black-Scholes Model)

空口無憑，我們用 Python 的 Black-Scholes 模型來證明上述理論。你可以直接複製以下代碼運行：

```python
import numpy as np
import pandas as pd
from scipy.stats import norm

# 1. 定義 Black-Scholes Call Price Function
def black_scholes_call(S, K, T, r, sigma):
    """
    S: Spot Price (標的資產價格)
    K: Strike Price (行使價)
    T: Time to Maturity (到期時間，年)
    r: Risk-free rate (無風險利率)
    sigma: Volatility (波動率/IV)
    """
    if T <= 0:
        return max(0, S - K)

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = (S * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
    return call_price

# 2. 設定參數 (HSI Context)
S0 = 27000  # 當前 HSI
r = 0.0418  # 無風險利率 (US 10Y)
sigma = 0.2143  # 引伸波幅 (IV)
strikes = np.arange(26000, 28100, 100)

# 設定兩種策略的到期日 (年)
days_weekly = 5
T_weekly = days_weekly / 252
days_monthly = 45
T_monthly = days_monthly / 252

# 3. 建立 DataFrame 模擬數據
df = pd.DataFrame({'Strike': strikes})

# --- 初始狀態 (Day 0) ---
df['Call_Weekly_T0'] = df.apply(lambda x: black_scholes_call(S0, x['Strike'], T_weekly, r, sigma), axis=1)
df['Call_Monthly_T0'] = df.apply(lambda x: black_scholes_call(S0, x['Strike'], T_monthly, r, sigma), axis=1)

# --- 劇本 1: 橫盤 5 天 (Sideways) ---
S_sideways = 27000
T_weekly_end = 0.00001  # Weekly 接近歸零
T_monthly_end = (days_monthly - 5) / 252

df['Call_Weekly_Sideways'] = df.apply(lambda x: black_scholes_call(S_sideways, x['Strike'], T_weekly_end, r, sigma), axis=1)
df['Call_Monthly_Sideways'] = df.apply(lambda x: black_scholes_call(S_sideways, x['Strike'], T_monthly_end, r, sigma), axis=1)

# 計算 ROI %
df['ROI_Weekly_Sideways'] = (df['Call_Weekly_Sideways'] - df['Call_Weekly_T0']) / df['Call_Weekly_T0'] * 100
df['ROI_Monthly_Sideways'] = (df['Call_Monthly_Sideways'] - df['Call_Monthly_T0']) / df['Call_Monthly_T0'] * 100

# --- 劇本 2: 明日大升 500 點 (Gap Up) ---
S_gapup = 27500
T_weekly_gap = (days_weekly - 1) / 252
T_monthly_gap = (days_monthly - 1) / 252

df['Call_Weekly_GapUp'] = df.apply(lambda x: black_scholes_call(S_gapup, x['Strike'], T_weekly_gap, r, sigma), axis=1)
df['Call_Monthly_GapUp'] = df.apply(lambda x: black_scholes_call(S_gapup, x['Strike'], T_monthly_gap, r, sigma), axis=1)

# 計算 ROI %
df['ROI_Weekly_GapUp'] = (df['Call_Weekly_GapUp'] - df['Call_Weekly_T0']) / df['Call_Weekly_T0'] * 100
df['ROI_Monthly_GapUp'] = (df['Call_Monthly_GapUp'] - df['Call_Monthly_T0']) / df['Call_Monthly_T0'] * 100

# 4. 打印關鍵結果
cols = ['Strike', 'ROI_Weekly_Sideways', 'ROI_Weekly_GapUp', 'ROI_Monthly_Sideways', 'ROI_Monthly_GapUp']
print(df[df['Strike'].isin([27000, 27200, 27400, 27600])][cols].round(1).to_string(index=False))