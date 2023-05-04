from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404

def archive(request):
	return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
	try:
		post = Article.objects.get(id=article_id)
		return render(request, 'article.html', {"post": post})
	except Article.DoesNotExist:
		raise Http404

def create_post(request):
	print(request.user)
	if not request.user.is_anonymous:
		if request.method == "POST":
			form = {
				'text': request.POST["text"], 'title': request.POST["title"]
			}
		# в словаре form будет храниться информация, введенная пользователем
			if form["text"] and form["title"]:
				#title is not unique
				if title_exist(form["title"]):
					form['errors'] = u"Статья с таким названием уже существует"
					return render(request, 'create_post.html', {'form': form})
		# если поля заполнены без ошибок
				new_article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
				return redirect('get_article', article_id=new_article.id)
			# перейти на страницу поста
			else:
		# если введенные данные некорректны
				form['errors'] = u"Не все поля заполнены"
				return render(request, 'create_post.html', {'form': form})
		else:
		# просто вернуть страницу с формой, если метод GET
			return render(request, 'create_post.html', {})

	else:
		raise Http404

def title_exist(title):
        try:
            Article.objects.get(title=title)
            return True
        except Article.DoesNotExist:
            return False

