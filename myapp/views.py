from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

next_id = 4
topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is ...'},
    {'id': 2, 'title': 'view', 'body': 'View is ...'},
    {'id': 3, 'title': 'model', 'body': 'Model is ...'}
]


def HTMLTemplate(articleTag, id=None):
    global topics
    context_ui = ''
    if id != None:
        context_ui = (f'''
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        ''')

    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'

    return (f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {ol}
            </ol>
            {articleTag}
            <ul>
                <li><a href="/create/">create</a></li>
                {context_ui}
            </ul>
        </body>
    </html>
    ''')


def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))


def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'

    return HttpResponse(HTMLTemplate(article, id))


@csrf_exempt
def create(request):
    global next_id
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea type="text" name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></input></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))

    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        new_topic = {"id": next_id, "title": title, "body": body}
        topics.append(new_topic)
        url = '/read/' + str(next_id)
        next_id += 1
        return redirect(url)


@csrf_exempt
def update(request, id):
    global topics

    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selected_topic = {
                    "title": topic["title"],
                    "body": topic["body"]
                }

        article = (f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selected_topic['title']}></p>
                <p><textarea type="text" name="body" placeholder="body">{selected_topic['body']}</textarea></p>
                <p><input type="submit"></input></p>
            </form>
        ''')
        return HttpResponse(HTMLTemplate(article, id))

    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic["title"] = title
                topic["body"] = body
        return redirect(f'/read/{id}')


@csrf_exempt
def delete(request):
    global topics

    if request.method == 'POST':
        id = request.POST['id']
        new_topics = []
        for topic in topics:
            if topic['id'] != int(id):
                new_topics.append(topic)
        topics = new_topics

        return redirect('/')
