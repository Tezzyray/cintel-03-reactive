


import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from shiny import render, reactive
import seaborn as sns

import pandas as pd

# Load palmer penguins data set
penguins_df = load_penguins()  # Use the function directly without specifying the module

# Set title page
ui.page_opts(title="Teslim", fillable=True)

# Create sidebar with open parameter and 2nd level header
with ui.sidebar(open="open"):
    ui.input_slider("selected_number_of_bins", "Number of Bins", 0, 100, 10)
    ui.h2("Sidebar")

    # Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 20)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Number of Seaborn bins", 0, 100, 20)

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr("Number of Seaborn bins")

    # Use ui.a() to add a hyperlink to the sidebar
    ui.a("GitHub",
        href="https://github.com/Tezzyray/cintel-02-data",
        target="_blank",)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group(
        "selected_species_list",
        "Select Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True
    )
    
    
# Data Grid
with ui.h2("Data Grid"):
    @render.data_frame
    def penguins_data_grid():
        return render.DataGrid(filtered_data(), height=150,)

# Data Table
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_data_table():
            return render.DataTable(filtered_data(), height=100)

# Plotly Histogram
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Penguin Histogram"):
        @render_plotly
        def plotly_histogram():
            plotly_hist = px.histogram(
                data_frame=filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species"
            ).update_layout(
                title="Plotly Penguins Data",
                xaxis_title="Selected Attribute",
                yaxis_title="Count"
            )
            return plotly_hist

# Seaborn Histogram
    with ui.nav_panel("Seaborn Histogram"):
        @render.plot
        def seaborn_histogram():
            seaborn_hist = sns.histplot(
                data=filtered_data(),
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )
            seaborn_hist.set_title("Seaborn Penguin Data")
            seaborn_hist.set_xlabel("Selected Attribute")
            seaborn_hist.set_ylabel("Count")
            return seaborn_hist

# Plotly Scatterplot
    with ui.nav_panel("Plotly Scatterplot"):
        ui.card_header("Plotly Scatter Plot Species")

        @render_plotly
        def plotly_scatterplot():
            plotly_scatter = px.scatter(
                penguins_df,
                x="bill_depth_mm",
                y="bill_length_mm",
                color="species",
                size_max=8,
                labels={
                    "bill_depth_mm": "Bill Depth(mm)",
                    "bill_length_mm": "Bill Length(mm)"
                }
            )
            return plotly_scatter
# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

    @reactive.calc
    def filtered_data():
        return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
