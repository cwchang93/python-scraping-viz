# 第 0 章｜開始自學：教材怎麼用、要會哪些 Python

這章是給自學者的入口。只要你看得懂基本 Python 程式，就可以開始；不用等到把所有資料分析課程上完。遇到不熟的概念，先用本章的對照表回到 Python Tutorial 複習，再回來繼續。

## 這門課在學什麼

爬蟲是用程式向網頁或資料服務取得資料。取得資料只是第一步，完整流程通常是：

```text
確認資料來源與規則 → 發出請求 → 讀懂回應 → 解析資料 → 清理與檢查 → 儲存 → 分析與呈現
```

有些頁面會用 JavaScript 才載入資料，或提供 JSON API；這時要先判斷適合用 `requests`、API 還是 Selenium。課程也會練習圖片與檔案下載。學習目標是理解每一步、能修改程式並檢查結果，而不是背下所有套件語法。

## 開始前的 Python 自我檢查

你不必一開始就精通所有項目。以下是進入 Lesson 01 前建議能看懂或查著寫出的基本能力：

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

若上述多數項目都陌生，建議先完成 Python Tutorial 的第 2–10 堂；不必因此延後開始，可以先讀 Lesson 01，碰到不熟的語法再回去補。

## 後續會用到的資料分析基礎

Lesson 01–04 會從網路請求、HTML 和解析開始；Lesson 05 起會使用 pandas。要跟上後半段，建議逐步熟悉：

- **DataFrame、讀取 CSV、查看資料**：回看 [Python Tutorial 第 13 堂：表格與 CSV](../../../Python-Tutorial/course_v2/lessons/lesson13_tables_csv/README.md) 和 [第 14 堂：Pandas 與 DataFrame](../../../Python-Tutorial/course_v2/lessons/lesson14_pandas_dataframe/README.md)。
- **篩選、排序、分組**：回看 [第 15 堂：Pandas 選取與篩選](../../../Python-Tutorial/course_v2/lessons/lesson15_pandas_selection/README.md) 和 [第 17 堂：資料整理、統計與 NumPy](../../../Python-Tutorial/course_v2/lessons/lesson17_groupby_numpy/README.md)。
- **缺值、重複、字串與型態清理**：回看 [第 16 堂：資料清理](../../../Python-Tutorial/course_v2/lessons/lesson16_data_cleaning/README.md)。
- **Matplotlib 圖表**：回看 [第 18 堂：Matplotlib 與圖表選擇](../../../Python-Tutorial/course_v2/lessons/lesson18_visualization/README.md)；本專案課綱預計在 Lesson 15 起進入視覺化。

這些是分階段需要的能力，不必在爬蟲課開始前一次全部學完。各堂 README 會列出當堂先備條件。

## 安裝與準備

需要 Python 3.10 以上。先在終端機切換到本專案資料夾，再建立虛擬環境並安裝套件：

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell 請改用：.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

若電腦的 Python 指令是 `python3`，建立環境及執行 pip 時將 `python` 改成 `python3`。成功啟用後，終端機提示通常會出現 `(.venv)`。之後每次開始練習，先啟用這個環境。

## 每一堂建議照這個順序自學

1. 從專案首頁進入該堂 `README.md`，先看「學習成果」和「課前準備」，確認自己已具備先備能力。
2. 打開 `lessonNN_learning.py`，按由上到下的順序讀每個 `# %%` 單元。先預測輸出，再執行並比對。
3. 一般課程檔可在 VS Code 安裝 Python 與 Jupyter 擴充後按 **Run Cell**。先執行檔案前面的匯入和工作目錄設定，再往下執行。
4. 第 8、9 堂是 Selenium 腳本，不要逐格執行；從該堂資料夾的終端機執行 `python lesson08_learning.py` 或 `python lesson09_learning.py`。
5. 接著做 `lessonNN_exercises.py` 和 `lessonNN_homework.py`。練習檔會用 `assert` 或 PASS/FAIL 提示檢查部分結果；錯誤時先讀最後一行訊息，再回頭看相關單元。
6. 每題先自己完成再看講解或參考解答。部分教師版解答不會提供給學生。
7. 在每堂資料夾的 `output/` 查看自己產生的 CSV、圖片或紀錄檔，確認筆數、欄位和內容合理。

## 網路、快照與爬取規則

- `fixtures/` 是教材附的本機網頁、JSON、CSV 或圖片快照；可用來離線練習，也能避免網站改版影響初學練習。
- 部分 learning 示範會連到外部練習網站；連線失敗時先照單元說明改讀 fixtures，不要對網站重複大量請求。
- 只練習教材指定的練習站、開放資料或明確允許的公開資料。遵守網站規則、設定 timeout、控制頻率；遇到 403、登入牆或驗證碼就停止，不要嘗試繞過。
- Lesson 08–09 需要 Google Chrome；第一次執行時 Selenium 可能要下載 chromedriver，因此需要網路。若無法使用 Chrome，Lesson 09 README 也說明可用 HTML 快照練習部分解析內容。

## 遇到問題時

- `ModuleNotFoundError`：確認虛擬環境已啟用，再執行 `python -m pip install -r requirements.txt`。
- 找不到 `fixtures/`：從該堂 README 指示的工作目錄執行，或先執行 learning 檔案最前面的工作目錄設定格。
- 網路錯誤或 timeout：先確認當堂是否有本機快照可替代；不要縮短 timeout 後對網站連續重試。
- 語法或資料錯誤：先看錯誤訊息最後一行，確認出錯的變數型態、欄位名稱和路徑，再回看相鄰的 learning 單元。
- 不懂某個 Python 語法：用上面的對照表回到 Python Tutorial 複習該堂，再回來重做同一題。

## 接下來怎麼走

- [爬蟲課學習路徑](../../LEARNING_PATH.md)：按能力階段理解每一組課程的目的。
- [專案大綱](../../PROJECT_OVERVIEW.md)：查看從網頁到資料分析成果的全貌。
- [完整課綱](../../COURSE_SYLLABUS.md)：查看 20 堂課的主題和產出。
- [各堂教材入口](../../README.md#快速入口)：直接進入 Lesson 01–10。
