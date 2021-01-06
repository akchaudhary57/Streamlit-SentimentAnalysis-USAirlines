import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)
#st.title("Hello World!")
#st.markdown("## My first streamlit dashboard")

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.markdown("This application is a Steamlit dashboad to analyze the sentiment of tweets  🐦")

DATA_URL = 'Tweets.csv'
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data()

#st.write(data)

st.sidebar.subheader("Show random tweets")
random_tweet = st.sidebar.radio('Sentiment',('positive','negative','neutral'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown("#### Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type',['Histogram','Pie chart'],key ='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index,'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide",True):
    st.markdown('### Number of tweets by sentiment')
    if select == 'Histogram':
        fig = px.bar(sentiment_count,x= 'Sentiment', y = 'Tweets',color ='Tweets',height = 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values = 'Tweets',names= 'Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of day",0,23)
#hour = st.sidebar.number_input("Hour of day",min_value =1,max_value = 24)
modified_data = data[data["tweet_created"].dt.hour == hour]
if  st.sidebar.checkbox("Show raw data",False,key = '1'):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiments")
Multichoice = st.sidebar.multiselect('Pick airlines',('US Airways','United','American','Southwest','Delta','Virgin America'),
                key ='0')

if len(Multichoice)>0:
    choice = data[data.airline.isin(Multichoice)]
    fig_choice = px.histogram(choice,x='airline',y='airline_sentiment',histfunc = 'count',color= 'airline_sentiment',
                    facet_col ='airline_sentiment',labels = {'airline_sentiment':'Tweets'},height = 600,width = 800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiments?',('positive','neutral','negative'))

if not st.sidebar.checkbox("Close",True,key = "3"):
    st.header('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    word_preprocessed = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@')
                            and word != 'RT'])
    word_cloud = WordCloud(stopwords = STOPWORDS,background_color = 'white',height = 640,width = 800).generate(word_preprocessed)
    plt.imshow(word_cloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
