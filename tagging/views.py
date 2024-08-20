from django.shortcuts import render, redirect,get_object_or_404
from .models import Tag , TaggedContent
from .embedding_utils import embedding_model,get_relevant_tags

# Create your views here.


def initialize_tags(request):
    predefined_tags = ['technology', 'health', 'sports', 'education', 'finance', 'entertainment', 'politics', 'science', 'travel', 'fashion', 'food',  'environment',  'history',  'art', 'music', 'business', 'psychology', 'law', 'real estate',  'automotive']
    for tag in predefined_tags:
        embedding = embedding_model.encode(tag)
        Tag.objects.create(name=tag, embedding=embedding)
    return render(request, 'tagging/initialize.html')    



def tag_content(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        tag_names = get_relevant_tags(content, top_n=1)
        
        # Save new article with content
        new_article = TaggedContent(content=content)
        new_article.save()
        
        # Get tags from the database
        tags = Tag.objects.filter(name__in=tag_names)
        
        # Set tags for the new article
        new_article.tags.set(tags)
        
        # Redirect to the results page with the article's content and tags
        return render(request, 'tagging/tag_results.html', {
            'content': new_article.content,
            'tags': new_article.tags.all()  # Fetch all related tags
        })

    # Render the tag content form
    return render(request, 'tagging/tag_content.html')



def tagged_content_history(request):
    tagged_contents = TaggedContent.objects.all().order_by('-created_at')
    return render(request, 'tagging/tagged_content_history.html', {'tagged_contents': tagged_contents})


def tagged_content_detail(request, id):
    # Get the tagged content item or return 404 if not found
    item = get_object_or_404(TaggedContent, id=id)
    
    context = {
        'item': item
    }
    
    return render(request, 'tagging/content_detail.html', context)


def delete_tagged_content(request, id):
    if request.method == 'POST':
        item = get_object_or_404(TaggedContent, id=id)
        item.delete()
    return redirect('tagged_content_history')