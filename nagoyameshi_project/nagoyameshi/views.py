from django.shortcuts import render, redirect

from django.views import View


# クエリビルダ
from django.db.models import Q


# models.py の中の Restaurant クラスをimportするには？
#from .models import Restaurant

# models.py の中の Category クラスをimportするには？
#from .models import Category

# ↑2つは ↓ 1つで書ける
from .models import Restaurant, Category, Review, Favorite


# トップページで一覧表示をするビュー
# index.htmlをレンダリングするビューを作る
'''
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
'''

class IndexView(View):

    def get(self, request, *args, **kwargs):
    
        context = {}

        # 検索フォームに、カテゴリの選択肢を作るためにも、カテゴリの全データを取り出す。
        context["categories"]   = Category.objects.all()



        #クエリを初期化しておく。
        query   = Q() 
        # この時点では検索の条件が何もない。
        # なので、 Restaurant.objects.filter(query) = Restaurant.objects.all()

        # query に検索条件を加え ↓のようにfilterの引数として使う。
        #  Restaurant.objects.filter(query)





        #検索キーワードがある場合のみ取り出す
        if "search" in request.GET:
            
            # "　A　洋食" → " A 洋食" → ["","A","洋食"]
            # "洋食　A" → "洋食 A" → [ "洋食","A" ]
            #全角スペースを半角スペースに変換、スペース区切りでリストにする。
            words   = request.GET["search"].replace("　"," ").split(" ")

            #クエリを追加する
            for word in words:

                #空欄の場合は次のループへ
                if word == "": 
                    continue

                #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
                #query &= Q(comment__contains=word)
                query &= Q(name__contains=word)
                # 最初は query の条件は空
                # 1回目のループで、 query &= Q(name__contains="洋食")
                # 2回目のループで、 query &= Q(name__contains="A")
                # 2回目のループが終わった時点の query は？  Restaurantのnameに、『洋食を含んでいる』なおかつ『Aを含んでいる』
        """
            # 作った条件を使って検索する。
            context["restaurants"] = Restaurant.objects.filter(query)
        else:
            # 全件出す。
            context["restaurants"] = Restaurant.objects.all()
            # この時点ではqueryは空の状態
            context["restaurants"] = Restaurant.objects.filter(query)
        """

        # TODO: カテゴリ検索をする。

        if "category" in request.GET:
            if request.GET["category"] != "":
                query &= Q(category=request.GET["category"])



        # 検索している場合もしていない場合も、Restaurant.objects.filter(query) でOK
        #作ったクエリを実行(検索のパラメータがない場合、絞り込みは発動しない。)
        #context["topics"] = Topic.objects.filter(query)
        context["restaurants"] = Restaurant.objects.filter(query)
        



        #return render(request,"bbs/index.html",context)
        return render(request,"nagoyameshi/index.html",context)

# urls.pyから呼び出せるようにする
index   = IndexView.as_view()


# 店舗の個別ページを表示させるビュー
class RestaurantView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {}

        # URLに含まれている整数がここで扱える。
        print(pk)

        # 店舗の個別ページなので pk( Restaurantのid)  を使って店舗検索をする。
        # .filter() で終わると、配列になってしまう。1個しかないのに配列になる。
        # .first() 配列から1番最初の要素を取る。
        context["restaurant"]   = Restaurant.objects.filter(id=pk).first()

        return render(request, "nagoyameshi/restaurant.html", context)

restaurant = RestaurantView.as_view()



class ReviewView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["review"]   = Review.objects.all()
        return render(request,"nagoyameshi/review.html",context)

review = ReviewView.as_view()





class FavoriteView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["favorite"]   = Favorite.objects.all()
        return render(request,"nagoyameshi/index.html",context)

favorite = FavoriteView.as_view()
