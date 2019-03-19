# block_business_account  

# 目的
近年学生を狙ったビジネスの勧誘がtwitterを通じて頻繁に行われている.  
ここで,自然言語処理の技術を応用してtwitterにおけるビジネスアカウントの自動ブロックアプリケーションを提案する.  

# 手法  
ビジネスアカウントのtweetデータ及びプロフィール文を取得  
前処理を行い文をモデルに入力  
文をembeddingしベクトル変換して入力する.  
正解データはそのツイート及びプロフィール文がビジネスアカウントであるか否かの2値  
学習済みモデルを用いて判定を行う  
ビジネスアカウント判定された場合自動的にブロックを行う
