from django.shortcuts import render

posts = [
{
    'author': 'Mehmet Ali Özcan',
    'title': 'Post 1',
    'content': 'It is the first post',
    'date_posted': '06.12.2022'
},
{
    'author': 'Gözde Bor Özcan',
    'title': 'Post 2',
    'content': 'It is the second post',
    'date_posted': '06.12.2022'
}
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')
