"""
This file contains functions for creating interactive visualizations, such as interactive time series plots using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def interactive_time_series(time_series_input, title='Time Series Plot'):
    """
    Creates an interactive time series plot using Plotly. Can handle a single time series or multiple time series.

    Args:
        time_series_input (list, np.ndarray, or list of lists/np.ndarray): The time series data to be plotted.
        title (str): The title of the plot.

    Returns:
        plotly.graph_objects.Figure: The interactive time series plot.
    """
    # Create a Plotly figure
    fig = go.Figure()

    # Check if the input is a single time series or a list of time series
    if isinstance(time_series_input[0], (list, np.ndarray)):
        # Multiple time series
        for i, time_series in enumerate(time_series_input):
            # Convert the time series to a NumPy array if it's a list
            if isinstance(time_series, list):
                time_series = np.array(time_series)

            # Generate x-axis values if not provided
            x_values = np.arange(len(time_series))

            # Add a line trace for the time series data
            fig.add_trace(go.Scatter(x=x_values, y=time_series, mode='lines', name=f'Series {i+1}'))
    else:
        # Single time series
        # Convert the time series to a NumPy array if it's a list
        if isinstance(time_series_input, list):
            time_series_input = np.array(time_series_input)

        # Generate x-axis values if not provided
        x_values = np.arange(len(time_series_input))

        # Add a line trace for the time series data
        fig.add_trace(go.Scatter(x=x_values, y=time_series_input, mode='lines'))

    # Update the layout with titles and axis labels
    fig.update_layout(title=title, xaxis_title='Time', yaxis_title='Amplitude')

    # Show the interactive plot
    fig.show()


def create_scatter_plot_matrix(df, title='Scatter Plot Matrix'):
    """
    Creates a scatter plot matrix from the given DataFrame.

    Args:
    df (DataFrame): The DataFrame containing the data to be plotted.
    title (str, optional): The title of the plot. Defaults to 'Scatter Plot Matrix'.

    Returns:
    None. Displays the plot.
    """
    # Create a scatter plot matrix using Plotly Express
    fig = px.scatter_matrix(df)
    # Update the layout of the figure with the provided title
    fig.update_layout(title=title)
    # Display the figure
    fig.show()