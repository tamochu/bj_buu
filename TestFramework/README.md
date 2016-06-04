# テストフレームワーク(作成中)
 - テストケースをテストする

## 使い方
 - testname.pmのファイル名でテストを書きローカルまたはリモートサーバーのテストフォルダに保存
 - TestFrameworkがテストを実行する
 - TestFrameworkはテスト実行の前後に任意でuser/log/dataフォルダの保存と復元を行う
 - TestFrameworkのUIはCUI版とブラウザ版がある

### テストの書き方
 - Controllerクラス(./Controller直下のクラス）のインスタンスメソッドを使って、疑似的なプレイのケースを書く
 - ./Tests/sample.pmにサンプルテストがある(まだない)

#### 構成
 + TestCUI(ローカルホストでテストを実行するUI  )
 
 + TestBrowser( サーバーにアップしたテストをブラウザ経由で実行するUI )
 
 + ./TestFramework
   + TestInterface(テストを実行するインターフェース)
   + /Controller(ユーザーがテストで使う抽象的な関数を持つクラスのフォルダ）
     + PlayerController
       + (プレイヤーデータの作成、削除、データ操作など)
     + CountryController
       + (国データの作成、削除、データ操作など)
     + WorldController
       + (世界情勢の変更や年度の変更など)
     + SystemController
       + (システム時刻の偽装やファイルの保存復元など)
      + ./Accessor(Adapterが使う実際にBJのCGIやデータにアクセスするクラスのフォルダ)
        + PlayerAccessor
        + CountryAccessor
        + etc...
    
 
