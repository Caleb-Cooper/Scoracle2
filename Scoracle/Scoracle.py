import streamlit as st
import numpy as np



# Set page configuration
st.set_page_config(
    page_title="Scoracle",
    page_icon="🔮",
    layout="centered"
)

# Home page content
st.markdown("# Welcome to Scoracle! 🔮")

# Sidebar navigation
page_options = {
    "Home": False,
    "📈 Plotting Demo": False,
    "🌍 Mapping Demo": False,
    "📊 DataFrame Demo": False
}

selected_page = st.sidebar.selectbox("Select a page:", list(page_options.keys()))

# Handle page navigation based on selection
for page_name in page_options:
    if selected_page == page_name:
        page_options[page_name] = True
    else:
        page_options[page_name] = False

# Render selected page content
if page_options["Home"]:
    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **🔮 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

elif page_options["📈 Plotting Demo"]:
    st.markdown("# Plotting Demo")
    st.write(
        """This demo illustrates a combination of plotting and animation with
    Streamlit. We're generating a bunch of random numbers in a loop for around
    5 seconds. Enjoy!"""
    )

    progress_bar = st.progress(0)
    status_text = st.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows

elif page_options["🌍 Mapping Demo"]:
    st.markdown("# Mapping Demo")
    st.write("This is the Mapping Demo content.")

elif page_options["📊 DataFrame Demo"]:
    st.markdown("# DataFrame Demo")
    st.write("This is the DataFrame Demo content.")

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
