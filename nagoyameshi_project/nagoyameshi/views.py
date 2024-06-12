from django.shortcuts import render

# Viewを継承したビュークラスを作る。(ListViewやCreateViewなどは、処理が抽象化されている(処理内容がわかりにくい)。)
from django.views import View


# index.htmlをレンダリングするビューを作る
class IndexView(View):

    def get(self, request, *args, **kwargs):

        #TODO: ここでRestaurantのモデルを扱う。

        # ページのレンダリング
        return render(request, "nagoyameshi/index.html")

# urls.pyから呼び出せるようにする
index   = IndexView.as_view()

