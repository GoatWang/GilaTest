# Q1-1
![answer](34470485_1740773745999083_7221755592874917888_n.jpg)

# Q1-2
1. F1-score: 
    - 如果拿到一個資料集，其中發現絕大多數的資料都是某一個類別，那麼一旦機器全部猜測那個類別，將可以得到相對較高的precision。
2. why not binary classification:
    - 因為，將導致activate fincation不平滑，進一步使得輸出結果非常極端，一但被分成特定類別，後面的back prop就很難修正。
3. bais and variance:
    - bais指得是演算法本身的假設錯誤逤導致的偏差，將導致model無法真正fit到正確的位置。variance指得是model對於資料的變動極度敏感而導致的偏差，當model過度fit在某一些資料上時，將會產勝這樣的問題。
4. 
5. onehot:
    - 指將類別資料轉換成0與1組成的向量。如[0,1,2] => [[1,0,0], [0,1,0], [0,0,1]]
6. overfitting:
    - Regularization: L1 or L2 norm，讓輸出結果正規劃。
    - dropout: 讓部份的node失去功效。雖然有看到論文說這是無效的作法，不過根據過去的經驗，還是有避免overfitting的功效。
    - 區分train test set: 讓部分資料不要放入model進行訓練，最後用test set來檢測是否有overfitting。
