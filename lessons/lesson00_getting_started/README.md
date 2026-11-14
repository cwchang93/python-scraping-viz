# 課程入口｜教材怎麼用、要會哪些 Python

這章是給自學者的入口。只要你看得懂基本 Python 程式，就可以開始；不用等到把所有資料分析課程上完。遇到不熟的概念，先用本章的對照表回到 Python Tutorial 複習，再回來繼續。

## 這門課在學什麼

爬蟲是用程式向網頁或資料服務取得資料。取得資料只是第一步，完整流程通常是：

```text
確認資料來源與規則 → 發出請求 → 讀懂回應 → 解析資料 → 清理與檢查 → 儲存 → 分析與呈現
```

有些頁面會用 JavaScript 才載入資料，或提供 JSON API；這時要先判斷適合用 `requests`、API 還是 Selenium。課程也會練習圖片與檔案下載。學習目標是理解每一步、能修改程式並檢查結果，而不是背下所有套件語法。

## 開始前的 Python 自我檢查

你不必一開始就精通所有項目。以下是進入 Lesson 02 前建議能看懂或查著寫出的基本能力；Lesson 01 會先透過練習喚回這些語法：

| Python 基礎 | 會用在哪裡 | 不熟時回看 Python Tutorial |
|---|---|---|
| 變數、字串、數字、布林值、型別轉換 | URL、網頁文字、價格與狀態碼 | [第 2 堂：變數、型別與運算](../../../Python-Tutorial/course_v2/lessons/lesson02_python_basics/README.md) |
| `if` / `elif` / `else`、比較與布林條件 | 判斷請求成功、欄位是否存在、資料是否符合條件 | [第 3 堂：條件判斷](../../../Python-Tutorial/course_v2/lessons/lesson03_conditions/README.md) |
| List、索引、切片、逐筆讀取 | 保存多筆網頁資料與分頁結果 | [第 4 堂：List 與 Tuple](../../../Python-Tutorial/course_v2/lessons/lesson04_list_tuple/README.md) |
| Dict、鍵值、`.get()` | 將每筆資料整理成欄位，讀取 JSON | [第 5 堂：Dict 與 Set](../../../Python-Tutorial/course_v2/lessons/lesson05_dict_set/README.md) |
| `for` 迴圈 | 逐筆解析網頁元素、逐頁抓取、批次下載 | [第 6 堂：for 迴圈](../../../Python-Tutorial/course_v2/lessons/lesson06_for_loops/README.md) |
| 函式、參數、回傳值 | 把抓取、解析和清理拆成可重用步驟 | [第 8 堂：函式](../../../Python-Tutorial/course_v2/lessons/lesson08_functions/README.md) |
| `try` / `except`、閱讀錯誤訊息 | 處理逾時、網路錯誤、欄位缺漏與格式問題 | [第 9 堂：錯誤處理與除錯](../../../Python-Tutorial/course_v2/lessons/lesson09_error_handling/README.md) |
| 匯入模組、路徑、讀寫文字檔與 CSV | 安裝套件、讀 fixtures、儲存爬取結果 | [第 10 堂：模組、檔案與 CSV](../../../Python-Tutorial/course_v2/lessons/lesson10_modules_files/README.md) |

若上述多數項目都陌生，建議先完成 Python Tutorial 的第 2–10 堂；也可以先做 Lesson 01 的暖身題，碰到不熟的語法再回去補。

## 後續會用到的資料分析基礎

Lesson 02–05 會從網路請求、HTML 和解析開始；Lesson 06 起會使用 pandas。要跟上後半段，建議逐步熟悉：

- **DataFrame、讀取 CSV、查看資料**：回看 [Python Tutorial 第 13 堂：表格與 CSV](../../../Python-Tutorial/course_v2/lessons/lesson13_tables_csv/README.md) 和 [第 14 堂：Pandas 與 DataFrame](../../../Python-Tutorial/course_v2/lessons/lesson14_pandas_dataframe/README.md)。
- **篩選、排序、分組**：回看 [第 15 堂：Pandas 選取與篩選](../../../Python-Tutorial/course_v2/lessons/lesson15_pandas_selection/README.md) 和 [第 17 堂：資料整理、統計與 NumPy](../../../Python-Tutorial/course_v2/lessons/lesson17_groupby_numpy/README.md)。
- **缺值、重複、字串與型態清理**：回看 [第 16 堂：資料清理](../../../Python-Tutorial/course_v2/lessons/lesson16_data_cleaning/README.md)。
- **Matplotlib 圖表**：回看 [第 18 堂：Matplotlib 與圖表選擇](../../../Python-Tutorial/course_v2/lessons/lesson18_visualization/README.md)；本專案課綱預計在 Lesson 16 起進入視覺化。

這些是分階段需要的能力，不必在爬蟲課開始前一次全部學完。各堂 README 會列出當堂先備條件。

## 安裝與準備

需要 Python 3.10 以上。你可以用一般 Python 虛擬環境，或在教室已安裝的 Anaconda 環境中執行。兩種方式選一種即可。

### 一般 Python 虛擬環境

先在終端機切換到本專案資料夾，再建立環境並安裝套件：

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell 請改用：.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

若電腦的 Python 指令是 `python3`，建立環境及執行 pip 時將 `python` 改成 `python3`。成功啟用後，終端機提示通常會出現 `(.venv)`。之後每次開始練習，先啟用這個環境。

### Windows 教室電腦：Anaconda + VS Code

不需要另外安裝 Jupyter Notebook 桌面程式。用 VS Code 開啟本專案資料夾，安裝 VS Code 的 **Python** 和 **Jupyter** 擴充功能；再按 `Ctrl+Shift+P`，選擇 **Python: Select Interpreter**，指定教室已安裝的 Anaconda Python。Anaconda 完整安裝通常已包含 Jupyter；若 VS Code 無法啟動互動視窗，在 Anaconda Prompt 對目前使用的環境執行 `python -m pip install jupyter`。

選好 Python Interpreter 後，開啟 **Terminal → New Terminal**，讓 VS Code 開一個使用該環境的新終端機。若終端機預設是 PowerShell，可在終端機右上角的下拉選單切換成 **Command Prompt**（`cmd`）。先確認它使用 Anaconda Python，再安裝教材套件：

```bat
where python
python --version
python -m pip install -r requirements.txt
```

`where python` 顯示的路徑應位於 Anaconda 安裝資料夾。若顯示找不到 `python` 或路徑指向其他 Python，從 **Anaconda Prompt** 切換到專案資料夾後執行 `code .`，再於 VS Code 開啟 Terminal：

```bat
cd /d "C:\你的路徑\python-scraping-viz"
code .
```

若資訊人員尚未替教室設定專用環境，可先在 Anaconda Prompt 建立一次，之後在 VS Code 的 **Python: Select Interpreter** 選取 `scraping`：

```bat
conda create -n scraping python=3.11
conda activate scraping
python -m pip install -r requirements.txt
python -m pip install jupyter
```

在 VS Code 開啟對應的 `.ipynb` 並逐格執行。第 9、10 堂先執行設定與函式定義，再執行示範格；每次示範會關閉瀏覽器與練習站。教室電腦若會重置，請資訊人員預先準備擴充功能、Python 環境、課程套件與 Chrome。

## 每一堂建議照這個順序自學

1. 從專案首頁進入該堂 `README.md`，先看「學習成果」和「課前準備」，確認自己已具備先備能力。
2. 打開 `lessonNN_learning.ipynb`，由上到下閱讀並執行各格。先預測輸出，再執行並比對。
3. 在 VS Code 選好 Python 核心並安裝 Python、Jupyter 擴充。先執行前面的匯入和工作目錄設定，再往下執行。
4. 第 9、10 堂先執行設定與函式定義，再依序執行各示範格。
5. 接著做 `lessonNN_exercises.ipynb` 和 `lessonNN_homework.ipynb`。練習檔會用 `assert` 或 PASS/FAIL 提示檢查部分結果；錯誤時先讀最後一行訊息，再回頭看相關單元。
6. 每題先自己完成再看講解或參考解答。部分教師版解答不會提供給學生。
7. 在每堂資料夾的 `output/` 查看自己產生的 CSV、圖片或紀錄檔，確認筆數、欄位和內容合理。

## 網路、快照與爬取規則

- `fixtures/` 是教材附的本機網頁、JSON、CSV 或圖片快照；可用來離線練習，也能避免網站改版影響初學練習。
- 部分 learning 示範會連到外部練習網站；連線失敗時先照單元說明改讀 fixtures，不要對網站重複大量請求。
- 只練習教材指定的練習站、開放資料或明確允許的公開資料。遵守網站規則、設定 timeout、控制頻率；遇到 403、登入牆或驗證碼就停止，不要嘗試繞過。
- Lesson 09–10 需要 Google Chrome；第一次執行時 Selenium 可能要下載 chromedriver，因此需要網路。若無法使用 Chrome，Lesson 10 README 也說明可用 HTML 快照練習部分解析內容。

## 遇到問題時

- `ModuleNotFoundError`：確認虛擬環境已啟用，再執行 `python -m pip install -r requirements.txt`。
- 找不到 `fixtures/`：從該堂 README 指示的工作目錄執行，或先執行 learning 檔案最前面的工作目錄設定格。
- 網路錯誤或 timeout：先確認當堂是否有本機快照可替代；不要縮短 timeout 後對網站連續重試。
- 語法或資料錯誤：先看錯誤訊息最後一行，確認出錯的變數型態、欄位名稱和路徑，再回看相鄰的 learning 單元。
- 不懂某個 Python 語法：用上面的對照表回到 Python Tutorial 複習該堂，再回來重做同一題。

## 接下來怎麼走

- [爬蟲課學習路徑](../../LEARNING_PATH.md)：按能力階段理解每一組課程的目的。
- [專案大綱](../../PROJECT_OVERVIEW.md)：查看從網頁到資料分析成果的全貌。
- [完整課綱](../../COURSE_SYLLABUS.md)：查看 21 堂課的主題和產出。
- [各堂教材入口](../../README.md#快速入口)：直接進入 Lesson 01–11。
