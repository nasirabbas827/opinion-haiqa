from django.contrib import admin
from .models import user_register, Post, Comment
from nltk.tokenize import word_tokenize
from nltk.corpus import sentiwordnet as swn, stopwords

admin.site.register(user_register)
admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'post', 'text', 'sentiment_label', 'sentiment_score', 'comment_date')
    readonly_fields = ('sentiment_label', 'sentiment_score')  # Make sentiment fields read-only
    exclude = ('sentiment_label', 'sentiment_score')  # Exclude sentiment fields from the form

    def save_model(self, request, obj, form, change):
        # Calculate sentiment score and label before saving
        if not obj.sentiment_score and not obj.sentiment_label:
            sentiment_score, sentiment_label = calculate_sentiment(obj.text)
            obj.sentiment_score = sentiment_score
            obj.sentiment_label = sentiment_label
        super().save_model(request, obj, form, change)


def calculate_sentiment(text):
    # Calculate sentiment score and label
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in tokens if word.isalpha() and word not in stop_words]

    positive_score = 0
    negative_score = 0
    for word in filtered_words:
        synsets = list(swn.senti_synsets(word))
        if synsets:
            synset = synsets[0]  # Use the first synset for simplicity
            positive_score += synset.pos_score()
            negative_score += synset.neg_score()

    sentiment_score = positive_score - negative_score
    if sentiment_score > 0:
        sentiment_label = 'Positive'
    elif sentiment_score < 0:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return sentiment_score, sentiment_label
