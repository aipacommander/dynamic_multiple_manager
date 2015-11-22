とあるサイトのコードに毛を生やしただけのコード
苦情がきたら取り下げます。


# Centos6.2で動作させるときにやったこと

## 必要ライブラリのインストール

```sh
$ pip install chardet
$ pip install BeautifulSoup
```


### Image系

```sh
$ yum install -y libjpeg-devel
$ easy_install PIL
$ pip install Image
```

## 実行

```sh
$ python2.7 get_dmm_id.py >/dev/null 2>&1 &
```