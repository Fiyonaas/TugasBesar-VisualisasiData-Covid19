# Fiyona Anmila Syamsir
# 1301194201
# IF-42-GAB04


# import library yang akan dibutuhkan
import pandas as pd
import datetime as dt
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, row
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import DateRangeSlider, Select
from bokeh.models.widgets import Tabs, Panel


# load data
dataset = pd.read_csv("./data/dataset-covid19.csv")
# mengatur index berdasarkan kolom Location Level yang berlabel Country
index = dataset[dataset["Location Level"] == "Country"].index
# menjadikan index sama dengan label
dataset.drop(index,axis=0,inplace=True)


# menampung data yang ingin diolah berdasarkan 12 kolom pertama
df_covid = dataset.iloc[:,:12]
# menghapus kolom yang tidak dibutuhkan
kolom = ["Location Level", "Location ISO Code", "New Deaths", "Total Cases"]
df_covid.drop(kolom,axis=1,inplace=True)


# mengubah nama kolom
nm_kolom = {
    "New Active Cases":"New_Active_Cases",
    "New Cases":"New_Cases",
    "New Recovered":"New_Recovered",
    "Total Active Cases":"Total_Active_Cases",
    "Total Recovered":"Total_Recovered",
    "Total Deaths":"Total_Deaths"
}
df_covid.rename(nm_kolom,axis=1,inplace=True)

# mengubah tipe pada kolom Date dari object menjadi datetime
df_covid["Date"] = pd.to_datetime(df_covid["Date"]).dt.date
df_covid["Location_STR"] = df_covid["Location"] 

# membuat list untuk parameter lokasi
x_lokasi = df_covid["Location"].value_counts().sort_index().index.tolist()


# mengelompokkan data berdasarkan kolom yang menjadi patokan
# saat menampilkan figure

# data kasus aktif baru
src_nacases = ColumnDataSource(data={
    'Date':df_covid[df_covid['Location']=='Jawa Barat']['Date'],
    'New_Active_Cases':df_covid[df_covid['Location']=='Jawa Barat']['New_Active_Cases']
})

# data kasus baru
src_ncases = ColumnDataSource(data={
    'Date':df_covid[df_covid['Location']=='Jawa Barat']['Date'],
    'New_Cases':df_covid[df_covid['Location']=='Jawa Barat']['New_Cases']
})

# data baru pasien sembuh 
src_nrecov = ColumnDataSource(data={
    'Date':df_covid[df_covid['Location']=='Jawa Barat']['Date'],
    'New_Recovered':df_covid[df_covid['Location']=='Jawa Barat']['New_Recovered']
})

# data total kasus aktif
src_tacases = ColumnDataSource(data={
    'Date':df_covid[df_covid['Location']=='Jawa Barat']['Date'],
    'Total_Active_Cases':df_covid[df_covid['Location']=='Jawa Barat']['Total_Active_Cases']
})


# data total sembuh 
src_tcases = ColumnDataSource(data={
    'Date':df_covid[df_covid['Location']=='Jawa Barat']['Date'],
    'Total_Recovered':df_covid[df_covid['Location']=='Jawa Barat']['Total_Recovered']
})

# data total kematian 
src_tdeath = ColumnDataSource(data={
    'Date':df_covid[df_covid['Location']=='Jawa Barat']['Date'],
    'Total_Deaths':df_covid[df_covid['Location']=='Jawa Barat']['Total_Deaths']
})


# membuat tooltip untuk data acuan
tooltip_nacases = [
    ('Tanggal', '@Date{%F}'),
    ('Kasus Aktif Baru', '@New_Active_Cases')
]

tooltip_ncases = [
    ('Tanggal', '@Date{%F}'),
    ('Kasus Baru', '@New_Cases')
]

tooltip_nrecov = [
    ('Tanggal', '@Date{%F}'),
    ('Data Baru Pasien Sembuh', '@New_Recovered')
]

tooltip_tacases = [
    ('Tanggal', '@Date{%F}'),
    ('Total Kasus Aktif', '@Total_Active_Cases')
]


tooltip_tdeath = [
    ('Tanggal', '@Date{%F}'),
    ('Total Kematian', '@Total_Deaths')
]

# membuat figure untuk menampilkan diagram data yang diolah
fig_nacases = figure(x_axis_type='datetime',
                    title='Kasus Aktif Baru',
                    x_axis_label='Tanggal',
                    y_axis_label='Kasus Aktif Baru',
                    plot_height=500,
                    plot_width=750   
)

fig_ncases = figure(x_axis_type='datetime',
                    title='Kasus Baru',
                    x_axis_label='Tanggal',
                    y_axis_label='Kasus Baru',
                    plot_height=500,
                    plot_width=750   
)

fig_nrecov = figure(x_axis_type='datetime',
                    title='Data Baru Pasien Sembuh',
                    x_axis_label='Tanggal',
                    y_axis_label='Data Baru Pasien Sembuh',
                    plot_height=500,
                    plot_width=750   
)

fig_tacases = figure(x_axis_type='datetime',
                    title='Total Kasus Aktif',
                    x_axis_label='Tanggal',
                    y_axis_label='Total Kasus Aktif',
                    plot_height=500,
                    plot_width=750   
)


fig_tdeath = figure(x_axis_type='datetime',
                    title='Total Kematian',
                    x_axis_label='Tanggal',
                    y_axis_label='Total Kematian',
                    plot_height=500,
                    plot_width=750   
)


# menambah fitur hover
fig_nacases.add_tools(HoverTool(formatters={'@Date':'datetime'}, tooltips=tooltip_nacases))
fig_ncases.add_tools(HoverTool(formatters={'@Date':'datetime'}, tooltips=tooltip_ncases))
fig_nrecov.add_tools(HoverTool(formatters={'@Date':'datetime'}, tooltips=tooltip_nrecov))
fig_tacases.add_tools(HoverTool(formatters={'@Date':'datetime'}, tooltips=tooltip_tacases))
fig_tdeath.add_tools(HoverTool(formatters={'@Date':'datetime'}, tooltips=tooltip_tdeath))


# mengatur tampilan representasi data diagram ke dalam bentuk garis
fig_nacases.line('Date','New_Active_Cases',
                    source=src_nacases,
                    color='#0072BD'
)

fig_ncases.line('Date','New_Cases',
                    source=src_ncases,
                    color='#7E2F8E'
)

fig_nrecov.line('Date','New_Recovered',
                    source=src_nrecov,
                    color='#77AC30'
)

fig_tacases.line('Date','Total_Active_Cases',
                    source=src_tacases,
                    color='#D95319'
)


fig_tdeath.line('Date','Total_Deaths',
                    source=src_tdeath,
                    color='#A2142F'
)


# fungsi update data yang diacu
def update_nacases(attr,old,new):
    [start,end] = slider_nacases.value
    date_awal = dt.datetime.fromtimestamp(start/1000.0).date()
    date_akhir = dt.datetime.fromtimestamp(end/1000.0).date()
    data_lokasi = str(lokasi_nacases.value)

    # mengatur data baru
    date_loc = df_covid[(df_covid['Date'] >= date_awal) & (df_covid['Date'] <= date_akhir)]
    data_baru = {
        'Date' : date_loc[date_loc['Location']==data_lokasi]['Date'],
        'New_Active_Cases' : date_loc[date_loc['Location']==data_lokasi]['New_Active_Cases']
    }
    src_nacases.data = data_baru

def update_ncases(attr,old,new):
    [start,end] = slider_ncases.value
    date_awal = dt.datetime.fromtimestamp(start/1000.0).date()
    date_akhir = dt.datetime.fromtimestamp(end/1000.0).date()
    data_lokasi = str(lokasi_ncases.value)

    # mengatur data baru
    date_loc = df_covid[(df_covid['Date'] >= date_awal) & (df_covid['Date'] <= date_akhir)]
    data_baru = {
        'Date' : date_loc[date_loc['Location']==data_lokasi]['Date'],
        'New_Cases' : date_loc[date_loc['Location']==data_lokasi]['New_Cases']
    }
    src_ncases.data = data_baru

def update_nrecov(attr,old,new):
    [start,end] = slider_nrecov.value
    date_awal = dt.datetime.fromtimestamp(start/1000.0).date()
    date_akhir = dt.datetime.fromtimestamp(end/1000.0).date()
    data_lokasi = str(lokasi_nrecov.value)

    # mengatur data baru
    date_loc = df_covid[(df_covid['Date'] >= date_awal) & (df_covid['Date'] <= date_akhir)]
    data_baru = {
        'Date' : date_loc[date_loc['Location']==data_lokasi]['Date'],
        'New_Recovered' : date_loc[date_loc['Location']==data_lokasi]['New_Recovered']
    }
    src_nrecov.data = data_baru

def update_tacases(attr,old,new):
    [start,end] = slider_tacases.value
    date_awal = dt.datetime.fromtimestamp(start/1000.0).date()
    date_akhir = dt.datetime.fromtimestamp(end/1000.0).date()
    data_lokasi = str(lokasi_tacases.value)

    # mengatur data baru
    date_loc = df_covid[(df_covid['Date'] >= date_awal) & (df_covid['Date'] <= date_akhir)]
    data_baru = {
        'Date' : date_loc[date_loc['Location']==data_lokasi]['Date'],
        'Total_Active_Cases' : date_loc[date_loc['Location']==data_lokasi]['Total_Active_Cases']
    }
    src_tacases.data = data_baru


def update_tdeath(attr,old,new):
    [start,end] = slider_tdeath.value
    date_awal = dt.datetime.fromtimestamp(start/1000.0).date()
    date_akhir = dt.datetime.fromtimestamp(end/1000.0).date()
    data_lokasi = str(lokasi_tdeath.value)

    # mengatur data baru
    date_loc = df_covid[(df_covid['Date'] >= date_awal) & (df_covid['Date'] <= date_akhir)]
    data_baru = {
        'Date' : date_loc[date_loc['Location']==data_lokasi]['Date'],
        'Total_Deaths' : date_loc[date_loc['Location']==data_lokasi]['Total_Deaths']
    }
    src_tdeath.data = data_baru



# fitur memilih lokasi pada setiap diagram yang diacu
lokasi_nacases = Select(
    options=[str(x) for x in x_lokasi],
    value = 'Jawa Barat',
    title = 'Lokasi yang dituju:'
)

lokasi_ncases = Select(
    options=[str(x) for x in x_lokasi],
    value = 'Jawa Barat',
    title = 'Lokasi yang dituju:'
)

lokasi_nrecov = Select(
    options=[str(x) for x in x_lokasi],
    value = 'Jawa Barat',
    title = 'Lokasi yang dituju:'
)

lokasi_tacases = Select(
    options=[str(x) for x in x_lokasi],
    value = 'Jawa Barat',
    title = 'Lokasi yang dituju:'
)


lokasi_tdeath = Select(
    options=[str(x) for x in x_lokasi],
    value = 'Jawa Barat',
    title = 'Lokasi yang dituju:'
)


# mengatur data yang ditampilkan berdasarkan lokasi yang dipilih
lokasi_nacases.on_change('value',update_nacases)
lokasi_ncases.on_change('value',update_ncases)
lokasi_nrecov.on_change('value',update_nrecov)
lokasi_tacases.on_change('value',update_tacases)
lokasi_tdeath.on_change('value',update_tdeath)

# mengatur slider waktu pada diagram yang dituju
init_value = (df_covid['Date'].min(), df_covid['Date'].max())
slider_nacases = DateRangeSlider(start=init_value[0], end = init_value[1], value=init_value)
slider_ncases = DateRangeSlider(start=init_value[0], end = init_value[1], value=init_value)
slider_nrecov = DateRangeSlider(start=init_value[0], end = init_value[1], value=init_value)
slider_tacases = DateRangeSlider(start=init_value[0], end = init_value[1], value=init_value)
slider_tdeath = DateRangeSlider(start=init_value[0], end = init_value[1], value=init_value)


# mengatur data pada slider saat parameter diubah
slider_nacases.on_change('value', update_nacases)
slider_ncases.on_change('value',update_ncases)
slider_nrecov.on_change('value',update_nrecov)
slider_tacases.on_change('value',update_tacases)
slider_tdeath.on_change('value',update_tdeath)

# mengatur tampilan diagram dan fitur dari data yang diacu
layout_nacases = row(widgetbox(lokasi_nacases, slider_nacases), fig_nacases)
layout_ncases = row(widgetbox(lokasi_ncases, slider_ncases), fig_ncases)
layout_nrecov = row(widgetbox(lokasi_nrecov, slider_nrecov), fig_nrecov)
layout_tacases = row(widgetbox(lokasi_tacases, slider_tacases), fig_tacases)
layout_tdeath = row(widgetbox(lokasi_tdeath, slider_tdeath), fig_tdeath)

# menambahkan fitur tabs
panel_nacases = Panel(child=layout_nacases, title='Kasus Aktif Baru')
panel_ncases = Panel(child=layout_ncases, title='Kasus Baru')
panel_nrecov = Panel(child=layout_nrecov, title='Data Baru Pasien Sembuh')
panel_tacases = Panel(child=layout_tacases, title='Total Kasus Aktif')
panel_tdeath = Panel(child=layout_tdeath, title='Total Kematian')
tabs = Tabs(tabs=[panel_nacases,panel_ncases,panel_nrecov,panel_tacases,panel_tdeath])

curdoc().add_root(tabs)

# untuk menjalankan aplikasi bokeh ini secara local, lakukan command 'bokeh serve --show myapp.py' di terminal