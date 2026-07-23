import streamlit as st 
import preprocessor
import helper
import matplotlib.pyplot as plt 
import plotly.express as px
import seaborn as sns

st.sidebar.title('Whatsaap chat Analyzer')

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data= uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    # st.dataframe(df)

    #  fetch unique users 
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button('Show Analysis'):
        num_messages, words,num_media_messages , number_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1 ,col2 ,col3 ,col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total words')
            st.title(words)    
        with col3:
            st.header('Media shared')
            st.title(num_media_messages) 
        with col4:
            st.header('links Shared')  
            st.title(number_links)  


        #monthly time-line 
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax= plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline 
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color="red",linewidth=2)
        ax.set_title("Daily Message Timeline", fontsize=16, fontweight='bold')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Messages", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        st.pyplot(fig)


        #activity map 
        st.title("Activity Map")
        col1 ,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index , busy_day.values,color="green")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index , busy_month.values,color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heatmap 
        st.title("weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user , df)
        fig ,ax =plt.subplots(figsize=(12,6))
        ax =sns.heatmap(user_heatmap,ax=ax , cmap="YlGnBu",linewidths=0.5 , linecolor='white')
        plt.tight_layout()
        ax.set_title("Weekly Activity Heatmap", fontsize=16, fontweight="bold")
        st.pyplot(fig)


        # finding the busiest users in the group(group level)   ///python -m streamlit run app.py

        if selected_user == 'Overall':
            st.title('Most busy Users')
            x,new_df= helper.fetch_most_busy_users(df)
            fig , ax = plt.subplots()
            col1 ,col2 = st.columns(2) 
            with col1 :
                ax .bar(x.index ,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)    

        # Wordclod 
        st.title('Wordcloud')
        df_wc =helper.creat_wordcloud(selected_user ,df)
        fig,ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words 
        st.title('Most common words')
        most_common_df = helper.most_common_words(selected_user ,df)
        fig , ax = plt.subplots()
        plt.xticks(rotation='vertical')
        ax.bar(most_common_df[0],most_common_df[1])
        st.pyplot(fig)

        st.dataframe(most_common_df)


        #  emoji analysis 
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user , df)
        # st.dataframe(emoji_df)

        col1 , col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            # fig ,ax = plt.subplots()
            # ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct="%0.2f") 
            # st.pyplot(fig)   
            # fig, ax = plt.subplots(figsize=(6,4))
            # ax.bar(emoji_df[0].head(), emoji_df[1].head())
            # st.pyplot(fig)
            fig = px.pie(
                emoji_df.head(10),
                names=0,
                values=1,
                title="Top 10 Most used Emojis"
            )
            
            st.plotly_chart(fig, use_container_width=True)




