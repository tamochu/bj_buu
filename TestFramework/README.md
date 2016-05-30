# テストフレームワーク
 - テストケースをテストする
 - 既存
## 使い方
 - testname.pmのファイル名でテストを書きローカルまたはリモートサーバーのテストフォルダに保存
 - TestFrameworkがテストを実行する
 - TestFrameworkはテスト実行の前後に任意でuser/log/dataフォルダの保存と復元を行う
 - TestFrameworkのUIはCUI版とブラウザ版がある

### テストの書き方
 - AccessAdapterクラスのインスタンスメソッドを使って、疑似的なプレイのケースを書く
 - ./Tests/sample.pmにサンプルテストがある

### 構成
 + TestCUI( ローカルホストでテストを実行するUI  )
 + TestBrowser( サーバーにアップしたテストをブラウザ経由で実行するUI )
 + TestFramework(テストを実行するフレームワーククラス)
   + Adapter(テストで使う関数を持つクラス)
     + PlayerAccessAdapter(プレイヤーデータの作成、削除、操作など)
     + CountryAccessAdapter(国データの作成、削除、操作など)
     + WorldAccessAdapter(世界情勢の変更や年度の変更など)
     + SystemAccessAdapter(システム時刻の偽装やファイルの保存復元など)
     + Accessor(BJのデータを読み書きするクラス)
 
