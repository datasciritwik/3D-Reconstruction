import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
# import matplotlib.pyplot as plt
# from streamlit_option_menu import option_men

st.set_page_config(layout='wide')
a = """
<style>
#MainMenu {visibility : hidden; }
footer {visibility : hidden; }
</style>
"""
st.markdown(a, unsafe_allow_html=True)

def norm_func(x):
    return (x-x.min())/(x.max()-x.min())

##F5D7AF-heading
##782D2D-page-bg
##C87D5A-textC

# [theme]
# primaryColor="#aa5656"
# backgroundColor="#d2ab83"
# secondaryBackgroundColor="#8b8b9c"
# textColor="#080808"
# font="serif"

st.markdown("<h1 style='text-align: center; color: #782D2D;'>2D/3D Reconstruction Dashboard</h1>", unsafe_allow_html=True)
l, r = st.columns(2)
with l:
    sidebar = st.radio('', ['HOME','Training Results'])
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)


##
def main():

    if sidebar == 'HOME':
        col1, col2, col3 = st.columns(3)
        col2.image('image.png', width=1000, use_column_width=True)

        ccol1, ccol2 = st.columns(2)
        with ccol1:
            st.subheader('Image Details')
            c1, c2, c3 = st.columns(3)
            c1.metric("Width", value='4946 pixels', help="Values can be dynamically")
            c2.metric("Height", value='3286 pixels', help="Values can be dynamically")
            c3.metric("Channel", value=3)
            c4, c5, c6 = st.columns(3)
            c4.metric("Bit Depth", value=24)
            c5.metric("Resolution", value='72 dpi', help="Values can be changed dynamically")
            c6.metric("Focal Lenght", value='35 mm', help="Values can be changed dynamically")
            c7, c8 = st.columns(2)
            c7.metric('Total Number of Images', '194', help="Values can be changed dynamically")
        with ccol2:
            st.subheader('Training Details')
            c7, c8, c9 = st.columns(3)
            c7.metric('Precision', 'fp16')
            c8.metric('Batch Size', value=2**16, help="Values can be changed dynamically")
            c9.metric('Total Number of Steps', '25000', help="Values can be changed dynamically")

            c10, c11, c12 = st.columns(3)
            c10.metric('Mesh Vertices', value=651245,delta=-8766593, help="Values can be changed dynamically")
            c11.metric('Mesh Faces', value=1163439,delta=-12377777, help="Values can be changed dynamically")
            c12.metric('Mesh Size', '500MB', help="Values can be changed dynamically")

            c13, c14, c15= st.columns(3)
            c13.metric('PSNR', value=30.11,delta=32.11, help="Values can be changed dynamically")
            c14.metric('SSIM', value=0.8208,delta=-0.7729, help="Values can be changed dynamically")


    if sidebar == "Training Results":
        l1, r1 = st.columns(2)
        with r1:
            l2, r2 = st.columns(2)
            with r2:
                project = st.selectbox('', ['METRICES PLOTS', 'STATISTICAL PLOTS'])

        df = pd.read_csv('plot_data.csv')
        if project == 'METRICES PLOTS':
            

            # Adding Columns
            col1, col2= st.columns(2, gap='large')
            
            with col1:
                # Plot the data using plotly
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=df['Timings'], y=df['Loss'], mode='markers+lines', name='Loss', line=dict(color='red')))
                fig1.update_layout(title='Loss vs. Timings', xaxis_title='Timings', yaxis_title='Loss')
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=df['Timings'], y=df['PSNR'], mode='markers+lines', name='PSNR', line=dict(color='green')))
                fig2.update_layout(title='PSNR vs. Timings', xaxis_title='Timings', yaxis_title='PSNR')
                st.plotly_chart(fig2, use_container_width=True)


            col3, col4 = st.columns(2, gap='large')
            with col3:
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(x=df['Timings'], y=df['Steps'], mode='markers+lines', name='Loss', line=dict(color='blue')))
                fig3.update_layout(title='Steps vs. Timings', xaxis_title='Timings', yaxis_title='Steps')
                st.plotly_chart(fig3, use_container_width=True)

            with col4:
                fig4 = go.Figure()
                fig4.add_trace(go.Scatter(x=df['Timings'], y=df['Learning_Rate'], mode='markers+lines', name='PSNR', line=dict(color='orange')))
                fig4.update_layout(title='Learning Rate vs. Timings', xaxis_title='Timings', yaxis_title='Learning Rate')
                st.plotly_chart(fig4, use_container_width=True)

            fig5 = go.Figure()
            fig5.add_trace(go.Scatter(x=df['Timings'], y=df['Rays_per_sec'], mode='markers+lines', name='PSNR', line=dict(color='#0A7D8C')))
            fig5.update_layout(title='Rays Per Second vs. Timings', xaxis_title='Timings', yaxis_title='Rays Per Second')
            st.plotly_chart(fig5, use_container_width=True)

        
        if project == 'STATISTICAL PLOTS':

            df1 = norm_func(df.iloc[:, 1:])
            df2 = pd.concat([df.iloc[:, :1], df1], axis=1)
            # col5, col6 = st.columns(2)
            new_labels = {
                'Timings': 'Time',
                'Steps' : 'No. of Steps',
                'Data' : 'Data',
                'Loss': 'Loss Value',
                'PSNR': 'PSNR Value',
                'Learning_Rate': 'Learning Rate',
                'Anti': 'Anti Value',
                'Dist': 'Dist Value',
                'Hash': 'Hash Value',
                'Rays_per_sec': 'Rays per Sec'
            }
            # st.line_chart(df1, use_container_width=True)
            # Create a Plotly figure
            fig = go.Figure()

            # Adding each line to the figure
            for col in df2.columns[1:]:
                fig.add_trace(go.Scatter(x=df2['Timings'], y=df2[col], mode='lines', name=new_labels[col]))

            # Update the layout
            fig.update_layout(title='Normalized Line Chart', xaxis_title='Timings', yaxis_title=None)

            # Display the figure using st.plotly_chart
            st.plotly_chart(fig, use_container_width=True)

            # with col6:
            # Calculate the correlation matrix
            correlation_matrix = df1.corr()

            # Rename column and index names

            correlation_matrix = correlation_matrix.rename(index=new_labels, columns=new_labels)

            # Create an interactive heatmap using plotly
            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                colorscale='RdBu',  # You can choose different color scales
                colorbar=dict(title='Correlation')
            ))

            fig.update_layout(title='Correlation Plot',
                            xaxis_title='Features',
                            yaxis_title='Features',
                            width=800,
                            height=600)

            st.plotly_chart(fig, use_container_width=True)


# if __name__=="__main__":
main()
