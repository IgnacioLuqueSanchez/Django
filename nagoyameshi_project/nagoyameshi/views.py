from django.shortcuts import render,redirect

# Viewを継承したビュークラスを作る。(ListViewやCreateViewなどは、処理が抽象化されている(処理内容がわかりにくい)。)
from django.views import View

from .models import Topic

# models.py の中の Restaurant クラスをimportするには？
#from .models import Restaurant

# models.py の中の Category クラスをimportするには？
#from .models import Category

# ↑2つは ↓ 1つで書ける
from .models import Restaurant,Category


# トップページで一覧表示をするビュー
# index.htmlをレンダリングするビューを作る
class IndexView(View):

    def get(self, request, *args, **kwargs):

        # ↓このTODOはアノテーション(注釈)コメント TODOはこれからやることをコメントとして書く。
        # XXX: 深刻なエラーが発生しているときのコメント
        # FIXME: 問題箇所

        context = {}

        # TODO: ここでRestaurantのモデルを扱う。
        # Restaurantの全データを読み込み
        context["restaurants"] = Restaurant.objects.all()
        # モデルクラス.objects.all()

        # TODO: ↑ 全データを取り出すのではなく、検索してデータを取り出しする。

        # 1: テンプレートの検索ボックスに書いた内容(検索キーワード)をビューで扱う
        # 2: 検索キーワードとモデルを使って検索処理をする

        # requestを使って検索ボックスに書いた内容を取り出す。
        # name="search" の場合、 request.GET["search"]
        # ただし、検索していない時、request.GET["search"] と呼び出すと、エラー
        if "search" in request.GET:
            print(request.GET["search"])
            # TODO: 検索処理をする。 .filter(検索条件) を使って検索できる
            context["restaurants"]  = Restaurant.objects.filter(name=request.GET["search"])
            # ↑ の場合、『洋食』 とだけ検索した時、何も出てこない。完全一致なので、出てこない

            # 『洋食』を含む検索をしたい時、 
            # `__contains`(大文字小文字の区別をする) `__icontains` (大文字と小文字の区別をしない)のいずれかを使う。
            context["restaurants"]  = Restaurant.objects.filter(name__icontains=request.GET["search"])
            #context["restaurants"]  = Restaurant.objects.filter(name__contains=request.GET["search"])

            # 『洋食　A』で検索しても、↑の場合、『洋食　A』を含むという意味になる。(『洋食』と『A』を含む検索ではない)
            # スペース区切りの検索
            # https://noauto-nolife.com/post/django-or-and-search/

        else:
            print("検索してない")



        # ページのレンダリング
        return render(request, "nagoyameshi/index.html", context)

# urls.pyから呼び出せるようにする
index   = IndexView.as_view()


# 店舗の個別ページを表示させるビュー
class RestaurantView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "nagoyameshi/restaurant.html", context)

restaurant = RestaurantView.as_view()

#TODO:クエリビルダをインポート
from django.db.models import Q

class IndexView(View):

    def get(self, request, *args, **kwargs):
        
        context = {}
        #クエリを初期化しておく。
        query   = Q()

        #検索キーワードがある場合のみ取り出す
        if "search" in request.GET:

            #全角スペースを半角スペースに変換、スペース区切りでリストにする。
            words   = request.GET["search"].replace("　"," ").split(" ")

            #クエリを追加する
            for word in words:

                #空欄の場合は次のループへ
                if word == "":
                    continue

                #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
                query &= Q(comment__contains=word)

        #作ったクエリを実行(検索のパラメータがない場合、絞り込みは発動しない。)
        context["topics"] = Topic.objects.filter(query)

        return render(request,"bbs/index.html",context)

index   = IndexView.as_view()