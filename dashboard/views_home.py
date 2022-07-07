from dashboard.views import Notification
import psutil
import time
import warnings
from datetime import datetime
from django.contrib.auth.decorators import login_required
from uptime import uptime
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.offline as offline
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from matplotlib.colors import Normalize
from plotly.graph_objs import *
from pygal.style import Style
import plotly
from .models import *
from django.conf import settings
import speedtest
from csv import writer


@login_required()
def akus_dashboard(request):
    if request.user.is_authenticated:
        nf = Notification()
        try:
            user = User.objects.filter(email=request.user.email)
            total_users = User.objects.count()
            web_websites = WebsiteLinks.objects.count()
            cctv_websites = Product.objects.count()
            total_websites = web_websites + cctv_websites
            uptime=""
            for data in user:
                # if data.group == 'admin' or data.group == 'developer':

                warnings.filterwarnings("ignore", category=DeprecationWarning)
                device_count = DeviceEquipement.objects.count()
                # uptime=uptime()
                
                # device_name = DeviceEquipement.objects.all()
                data_centers_count = DC.objects.count()

                # graph6 = pie_chart()
                # graph14 = pie_chart1()
                # graph16 = datetime1()
                # graph9 = solidgauge3()
                # graph10 = funnel()
                # graph11 = dot()
                # graph12 = radar()
                # graph7 = solidgauge1()
                # graph8 = solidgauge2()
                # graph5 = solidgauge()
                # graph13 = solidgauge4()
                # graph4 = subplots()
                # graph3 = axis_range()
                # graph2 = moving_tick()
                # graph = check_heatmap()
                # ---trap collector scattter graph function call to plot on home paage
                trap_collector = scattergraph()

                # --alerts and triggers
                # my_graph = graph_function()
                # plot_pie = pie_chart()

                full_solid_gauge = fullgauge()

                # sunburst_graph = sunburst()
                network_line_graph = line1()
                test1 = testgauge1()
                test2 = testgauge2()
                test3 = testgauge3()
                test4 = testgauge4()
                uptime_graph=line2()
                # test5 = testgauge5()
                # test6 = testgauge6()
                # test7 = testgauge7()
                # test8 = testgauge8()
                # barchart = bar_plot4()
                piechart = pie_chart2()
                barchart2 = bar_chart()
                UPtime=time.time()
                totalseconds=time.time()-psutil.boot_time()
                uptime11 = time.strftime('%dd', time.gmtime(totalseconds))
                uptime12 = time.strftime('%Hh', time.gmtime(totalseconds))
                uptime13 = time.strftime('%Mm', time.gmtime(totalseconds))
                # seconds = int(totalseconds % 60)

                
                # minutes=int(totalseconds % 3600)
                # hours=int(totalseconds % 86400)
                # days=int((totalseconds % (86400*30))/86400)

                # bar_chart
                # plot_bar_chart = bar_chart()
                context = {"udata": data, "date": datetime.now,'barchart2':barchart2,'piechart':piechart,
                            'total_users':total_users,'full_solid_gauge': full_solid_gauge,'total_websites':total_websites,
                            'data_centers_count':data_centers_count,'trap_collector': trap_collector,'network_line_graph': network_line_graph, 'device_count': device_count,'test1': test1, 'test2': test2, 'test3': test3, 'test4': test4, 'uptime11':uptime11,'uptime12':uptime12,'uptime13':uptime13,'uptime_graph':uptime_graph                    
                            }

                return render(request, "dashboard/akus1.html", context)
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
    else:
        return redirect('login_page')


# import plotly
from django.shortcuts import render

import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

def line2():
    import plotly
    import cufflinks as cf
    import pandas as pd
    uptime=[]


    List=[uptime]
    with open('dashboard/extraFiles/uptime.csv', 'a') as f_object:
        writer_object = writer(f_object)
        f_object.write("\n")
        writer_object.writerow(List)

        f_object.close()


    # setup
    layout1 = cf.Layout(
        height=300,
        width=450
    )
    cf.go_offline()
    df = pd.read_csv("dashboard/extraFiles/uptime.csv")

    network_line_plot = df.iplot(asFigure=True, kind='line', layout=layout1)

    config = {'displayModeBar': False}
    line2 = plotly.offline.plot(network_line_plot, output_type='div', config=config)
    return line2
def graph_function():
    labels = [1, 2, 3, 4]
    values = [10, 20, 30, 40]
    ndata = 100
    dfi = pd.DataFrame({'date': {0: '2020.01.01',
                                 1: '2020.01.01',
                                 2: '2020.01.01',
                                 3: '2020.01.01',
                                 4: '2020.01.01',
                                 5: '2020.01.01',
                                 6: '2020.02.01',
                                 7: '2020.02.01',
                                 8: '2020.02.01',
                                 9: '2020.02.01',
                                 10: '2020.02.01',
                                 11: '2020.02.01',
                                 12: '2020.03.01',
                                 13: '2020.03.01',
                                 14: '2020.03.01',
                                 15: '2020.03.01',
                                 16: '2020.03.01',
                                 17: '2020.03.01'},
                        'sub_id': {0: 1233,
                                   1: 1233,
                                   2: 1233,
                                   3: 3424,
                                   4: 3424,
                                   5: 3424,
                                   6: 1233,
                                   7: 1233,
                                   8: 1233,
                                   9: 3424,
                                   10: 3424,
                                   11: 3424,
                                   12: 1233,
                                   13: 1233,
                                   14: 1233,
                                   15: 3424,
                                   16: 3424,
                                   17: 3424},
                        'stat_type': {0: 'link_clicks',
                                      1: 'alerts',
                                      2: 'triggers',
                                      3: 'link_clicks',
                                      4: 'alerts',
                                      5: 'triggers',
                                      6: 'link_clicks',
                                      7: 'alerts',
                                      8: 'triggers',
                                      9: 'link_clicks',
                                      10: 'alerts',
                                      11: 'triggers',
                                      12: 'link_clicks',
                                      13: 'alerts',
                                      14: 'triggers',
                                      15: 'link_clicks',
                                      16: 'alerts',
                                      17: 'triggers'},
                        'value': {0: 12,
                                  1: 50,
                                  2: 9,
                                  3: 24,
                                  4: 100,
                                  5: 18,
                                  6: 14,
                                  7: 24,
                                  8: 39,
                                  9: 20,
                                  10: 10,
                                  11: 8,
                                  12: 4,
                                  13: 2,
                                  14: 3,
                                  15: 2,
                                  16: 1,
                                  17: 1}})

    # change some types
    dfi['date'] = pd.to_datetime(dfi['date'])
    dfi['sub_id'] = dfi['sub_id'].astype(str)
    df = dfi

    # split df by stat_type and organize them in a dict
    groups = df['stat_type'].unique().tolist()
    dfs = {}
    for g in groups:
        dfs[str(g)] = df[df['stat_type'] == g]

    # pivot data to get different sub_id across dates
    dfp = {}
    for df in dfs:
        dfp[df] = dfs[df].pivot(index='date', columns='sub_id', values='value')

    # one trace for each column per dataframe
    fig = go.Figure()

    # set up the first trace
    fig.add_trace(go.Scatter(x=dfp['link_clicks'].index,
                             y=dfp['link_clicks']['1233'],
                             visible=True)
                  )

    fig.add_trace(go.Scatter(x=dfp['link_clicks'].index,
                             y=dfp['link_clicks']['3424'],
                             visible=True)
                  )

    # plotly start
    # buttons for menu 1, names
    updatemenu = []
    buttons = []

    # button with one option for each dataframe
    for df in dfp.keys():
        buttons.append(dict(method='restyle',
                            label=df,
                            visible=True,
                            args=[{'y': [dfp[str(df)]['1233'].values, dfp[str(df)]['3424'].values],
                                   'x': [dfp[str(df)].index],
                                   'type': 'scatter'}],
                            )
                       )

    # some adjustments to the updatemenus
    updatemenu = []
    your_menu = dict()
    updatemenu.append(your_menu)
    updatemenu[0]['buttons'] = buttons
    updatemenu[0]['direction'] = 'down'
    updatemenu[0]['showactive'] = True

    # add dropdown menus to the figure
    fig.update_layout(showlegend=False, updatemenus=updatemenu)

    # add notations to the dropdown menus
    fig.update_layout(
        annotations=[
            go.layout.Annotation(text="<b>stat_type:</b>",
                                 x=-0.3, xref="paper",
                                 y=1.1, yref="paper",
                                 align="left", showarrow=False),
        ]
    )

    config = {'displayModeBar': False}

    plt_div = plotly.offline.plot(fig, output_type='div', config=config)

    return plt_div

def scattergraph():
    import plotly.express as px
    # import pandas as pd
    data = []
    time = []
    process = ProcessUtil.objects.all()
    for p in process:
        data.append(p.utilpercentage)
        time.append(p.time)
    mainData = {'time':time,'data':data}
    print(mainData)
    df = pd.DataFrame(mainData)
    print(df)
    fig = px.scatter(df, x="time", y="data", width=500, height=300)
    scatter_fig = fig.update_traces(marker=dict(size=12,
                                                line=dict(width=2,
                                                          color='Green')),
                                    selector=dict(mode='markers'))

    config = {'displayModeBar': False}
    scatter_plt_div = plotly.offline.plot(scatter_fig, output_type='div', config=config)

    return scatter_plt_div
def sunburst():
    import plotly.express as px
    df = px.data.tips()
    sunburst_fig = px.sunburst(df, path=['sex', 'day', 'time'], values='total_bill', color='day')

    config = {'displayModeBar': False}
    sunburst_plt_div = plotly.offline.plot(sunburst_fig, output_type='div', config=config)
    return sunburst_plt_div


def pie_chart():
    import plotly.express as px
    df = px.data.tips()
    fig = px.pie(df, values='tip', names='day', color='day',
                 color_discrete_map={'Thur': 'lightcyan',
                                     'Fri': 'cyan',
                                     'Sat': 'royalblue',
                                     'Sun': 'darkblue'})

    config = {'displayModeBar': False}
    pie_chart = plotly.offline.plot(fig, output_type='div', config=config)

    return pie_chart


def pie_chart1():
    import pygal
    pie_chart = pygal.Pie(inner_radius=.4, width=200, height=200)
    pie_chart.add('IE', 19.5, width=200, height=200)
    pie_chart.add('Firefox', 36.6, width=200, height=200)
    pie_chart.add('Chrome', 36.3, width=200, height=200)
    pie_chart.add('Safari', 4.5, width=200, height=200)
    pie_chart.add('Opera', 2.3, width=200, height=200)
    pie1 = pie_chart.render_data_uri()
    return pie1


def pie_chart2():
    import pygal
    hdd = psutil.disk_usage('/')
    total = hdd[0]/(1000000000)
    used = hdd[1]/(1000000000)
    free = hdd[2]/(1000000000)

    pie_chart = pygal.Pie(show_legend=False,
                          style=pygal.style.styles['default'](value_font_size=60))
    pie_chart.add('total', [total])
    pie_chart.add('used', [used])
    pie_chart.add('free', [free])
    # pie_chart.add('Safari', [4.4, .1])
    # pie_chart.add('Opera', [.1, 1.6, .1, .5])
    pie2 = pie_chart.render_data_uri()
    return pie2


def solidgauge():
    import pygal
    gauge = pygal.SolidGauge(
        half_pie=True,
        inner_radius=0.70,
        show_legend=False,
        width=100, height=100
    )
    gauge.add('', [{'value': 63, 'max_value': 100, 'color': 'lime', }])
    some_name = gauge.render_data_uri()
    return some_name


def datetime1():
    import pygal
    from datetime import datetime
    datetimeline = pygal.DateTimeLine(
        x_label_rotation=35, truncate_label=-1,
        x_value_formatter=lambda dt: dt.strftime('%d, %b %Y at %I:%M:%S %p'))
    datetimeline.add("Serie", [
        (datetime(2013, 1, 2, 12, 0), 300),
        (datetime(2013, 1, 12, 14, 30, 45), 412),
        (datetime(2013, 2, 2, 6), 823),
        (datetime(2013, 2, 22, 9, 45), 672)
    ])
    date1 = datetimeline.render_data_uri()
    return date1


def line1():
    import plotly
    import cufflinks as cf
    import pandas as pd
    formula = (10000000/1.192)
    st=speedtest.Speedtest()
    download =st.download()/formula
    upload=st.upload()/formula


    List=[download,upload]
    with open('dashboard/extraFiles/network.csv', 'a') as f_object:
        writer_object = writer(f_object)
        f_object.write("\n")
        writer_object.writerow(List)

        f_object.close()


    # setup
    layout1 = cf.Layout(
        height=300,
        width=450
    )
    cf.go_offline()
    df = pd.read_csv("dashboard/extraFiles/network.csv")

    network_line_plot = df.iplot(asFigure=True, kind='line', layout=layout1)

    config = {'displayModeBar': False}
    line1 = plotly.offline.plot(network_line_plot, output_type='div', config=config)
    return line1

def bar_plot4():
    import plotly.graph_objects as go

    x = ['b', 'a', 'c', 'd']
    fig = go.Figure(go.Bar(x=x, y=[2, 5, 1, 9], name='Montreal'))
    fig.add_trace(go.Bar(x=x, y=[1, 4, 9, 16], name='Ottawa'))
    fig.add_trace(go.Bar(x=x, y=[6, 8, 4.5, 8], name='Toronto'))

    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})

    config = {'displayModeBar': False}
    bar_chart = plotly.offline.plot(fig, output_type='div', config=config)

    return bar_chart

# Basic pie chart
def pie_chart():
    import plotly.express as px
    df = px.data.tips()
    fig10 = px.pie(df, values='tip', names='day', color='day', width=400, height=270,
                   color_discrete_map={'Thur': 'lightcyan',
                                       'Fri': 'cyan',
                                       'Sat': 'royalblue',
                                       'Sun': 'darkblue'})
    config = {'displayModeBar': False}
    pie_chart = plotly.offline.plot(fig10, output_type='div', config=config)

    return pie_chart


def bar_chart1():
    import plotly.express as px
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')

    config = {'displayModeBar': False}
    bar_chart1 = plotly.offline.plot(fig, output_type='div', config=config)

    return bar_chart1


def bar_chart():
    import pygal
    chrome = []
    firefox = []
    safari = []
    mozilla = []
    others = []
    browser = Browser.objects.all()
    for ch in browser:
        chrome.append(ch.chrome)
        firefox.append(ch.firefox)
        safari.append(ch.safari)
        mozilla.append(ch.mozilla)
        others.append(ch.others)
    # print(chrome)
    # print(firefox)
    # print(safari)
    # print(mozilla)
    # print(others)
        
    line_chart = pygal.Bar(show_legend=False,
                           style=pygal.style.styles['default'](value_font_size=60))
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2006))
    line_chart.add('Firefox', firefox)
    line_chart.add('Chrome', chrome)
    line_chart.add('safari',safari  )
    line_chart.add('Others', others)
    line_chart.add('mozilla', mozilla)
    bar = line_chart.render_data_uri()
    return bar


def solidgauge1():
    import pygal
    Solid_Gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70,
                                   show_legend=False)
    # Random data
    Solid_Gauge.add('A', [{'value': 1000, 'max_value': 2000}])
    Solid_Gauge.add('A', [{'value': 700, 'max_value': 2000}])
    Solid_Gauge.add('A', [{'value': 900, 'max_value': 2000}])

    Solid_Gauge.add('A', [{'value': 500, 'max_value': 2000}])
    Solid_Gauge.add('A', [{'value': 800, 'max_value': 2000}])
    # Solid_Gauge.add('A', [{'value': 900, 'max_value': 2000}])
    # Solid_Gauge.add('A', [{'value': 900, 'max_value': 2000}])

    # Solid_Gauge.add('A', [{'value': 900, 'max_value': 2000}])

    some_name1 = Solid_Gauge.render_data_uri()
    return some_name1


def testgauge1():
    import pygal
    vm = psutil.virtual_memory()[2]
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200,
                             show_legend=False)

    gauge.add('', [{'value': vm, 'max_value': 100, 'color': 'lime', }])
    some_name = gauge.render_data_uri()
    return some_name


def testgauge2():
    import pygal
    cp = psutil.cpu_percent()
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200, show_legend=False)
    gauge.add('', [{'value': cp, 'max_value': 100, 'color': 'red',}])
    some_name = gauge.render_data_uri()
    return some_name


def testgauge3():
    import pygal
    percent_formatter = lambda x: '{:.10g}GB'.format(x)
    svmem = psutil.virtual_memory() 
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200, show_legend=False)
    gauge.value_formatter = percent_formatter
    gauge.add('', [{'value': round(svmem.used/1024**3,2), 'max_value': round(svmem.total/1024**3,2), 'color': 'gold','label': 'Used'},{'value': round(svmem.available/1024**3,2), 'max_value': round(svmem.total/1024**3,2), 'color': 'green','label': 'Available'}
    ])
    some_name = gauge.render_data_uri()
    return some_name


def testgauge4():
    import pygal
    percent_formatter = lambda x: '{:.10g}%'.format(x)
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200, show_legend=False)
    gauge.value_formatter = percent_formatter
    gauge.add('', [{'value': psutil.cpu_percent(), 'max_value': 100, 'color': 'olive','label': 'CPU Usage'}])
    some_name = gauge.render_data_uri()
    return some_name


def testgauge5():
    import pygal
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200,
                             show_legend=False)

    gauge.add('', [{'value': 770, 'max_value': 1000, 'color': 'purple', }])
    some_name = gauge.render_data_uri()
    return some_name


def testgauge6():
    import pygal
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200, show_legend=False)
    gauge.add('', [{'value': 950, 'max_value': 1000, 'color': 'fuchsia', }])
    some_name = gauge.render_data_uri()
    return some_name


def testgauge7():
    import pygal
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200, show_legend=False)
    gauge.add('', [{'value': 669, 'max_value': 1000, 'color': 'aqua', }])
    some_name = gauge.render_data_uri()
    return some_name


def testgauge8():
    import pygal
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200, show_legend=False)
    gauge.add('', [{'value': 811, 'max_value': 1000, 'color': 'blue', }])
    some_name = gauge.render_data_uri()
    return some_name


def solidgauge2():
    import pygal
    gauge = pygal.SolidGauge(inner_radius=0.70)
    percent_formatter = lambda x: '{:.10g}%'.format(x)
    dollar_formatter = lambda x: '{:.10g}$'.format(x)
    gauge.value_formatter = percent_formatter

    gauge.add('Series 1', [{'value': 225000, 'max_value': 1275000}],
              formatter=dollar_formatter)
    gauge.add('Series 2', [{'value': 110, 'max_value': 100}])
    gauge.add('Series 3', [{'value': 3}])
    gauge.add(
        'Series 4', [
            {'value': 51, 'max_value': 100},
            {'value': 12, 'max_value': 100}])
    gauge.add('Series 5', [{'value': 79, 'max_value': 100}])
    gauge.add('Series 6', 99)
    gauge.add('Series 7', [{'value': 100, 'max_value': 100}])
    some_name2 = gauge.render_data_uri()
    return some_name2


def solidgauge3():
    from pygal.style import Style
    import pygal
    gauge_chart = pygal.Gauge(human_readable=True, width=270, height=150,
                              style=pygal.style.styles['default'](value_font_size=5))
    gauge_chart.custom_style = Style(
        background='transparent',
        plot_background='transparent',
        font_family='5',
        label_font_size='5',
        major_label_font_size='5',
        value_font_size='5',
        value_label_font_size='5',
        tooltip_font_size='5',
        title_font_size='5'
    )
    gauge_chart.range = [0, 10000]
    gauge_chart.add('Chrome', 8212)
    gauge_chart.add('Firefox', 8099)
    gauge_chart.add('Opera', 2933)
    gauge_chart.add('IE', 41)
    some_name3 = gauge_chart.render_data_uri()
    return some_name3

def solidgauge4():
    import pygal
    gauge = pygal.SolidGauge(
        half_pie=True,
        inner_radius=0.70,
        show_legend=False,
        width=100, height=100
    )
    gauge.add('', [{'value': 79, 'max_value': 100, 'color': 'red', }])
    some_name = gauge.render_data_uri()
    return some_name

def funnel():
    import pygal
    funnel_chart = pygal.Funnel()
    funnel_chart.title = 'V8 benchmark results'
    funnel_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay',
                             'NavierStokes']
    funnel_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    funnel_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    funnel_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])

    some_name4 = funnel_chart.render_data_uri()
    return some_name4

def dot():
    import pygal
    dot_chart = pygal.Dot(x_label_rotation=30)
    dot_chart.title = 'V8 benchmark results'
    dot_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay',
                          'NavierStokes']
    dot_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    dot_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    dot_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    dot_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
    some_name5 = dot_chart.render_data_uri()
    return some_name5

def radar():
    from pygal.style import Style
    import pygal
    radar_chart = pygal.Radar(width=350, height=220, style=pygal.style.styles['default'](value_font_size=5))
    radar_chart.custom_style = Style(
        background='transparent',
        plot_background='transparent',
        font_family='5')
    radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay',
                            'NavierStokes']
    radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
    some_name6 = radar_chart.render_data_uri()
    return some_name6

def subplots():
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import numpy as np

    N = 20
    x = np.linspace(0, 1, N)

    fig = make_subplots(1, 3)
    for i in range(1, 4):
        fig.add_trace(go.Scatter(x=x, y=np.random.random(N)), 1, i)
    fig.update_xaxes(matches='x')

    config = {'displayModeBar': False}
    plots = plotly.offline.plot(fig, output_type='div', config=config)

    return plots

def axis_range():
    import plotly.express as px
    import numpy as np

    x = np.linspace(1, 200, 30)
    fig = px.scatter(x=x, y=x ** 3, log_x=True, log_y=True, range_x=[0.8, 250])

    config = {'displayModeBar': False}
    axis = plotly.offline.plot(fig, output_type='div', config=config)

    return axis

def moving_tick():
    import plotly.express as px

    df = px.data.stocks(indexed=True) - 1
    fig = px.bar(df, x=df.index, y="GOOG")
    fig.update_yaxes(ticklabelposition="inside top", title=None)
    config = {'displayModeBar': False}
    movingtick = plotly.offline.plot(fig, output_type='div', config=config)

    return movingtick

def check_heatmap():
    import plotly.graph_objects as go
    import datetime
    import numpy as np
    np.random.seed(1)

    programmers = ['Alex', 'Nicole', 'Sara', 'Etienne', 'Chelsea', 'Jody', 'Marianne']

    base = datetime.datetime.today()
    dates = base - np.arange(180) * datetime.timedelta(days=1)
    z = np.random.poisson(size=(len(programmers), len(dates)))

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=dates,
        y=programmers,
        colorscale='Viridis'))

    heatmap_fig = fig.update_layout(
        title='GitHub commits per day',
        xaxis_nticks=36)

    config = {'displayModeBar': False}
    gauge_plt = plotly.offline.plot(heatmap_fig, output_type='div', config=config)

    return gauge_plt

def fullgauge():
    import pygal
    series=Series.objects.all()
 
    #change c
    gauge = pygal.SolidGauge(inner_radius=0.70, show_legend=False,
                             style=pygal.style.styles['default'](value_font_size=25))
    percent_formatter = lambda x: '{:.10g}%'.format(x)
    dollar_formatter = lambda x: '{:.10g}$'.format(x)
    gauge.value_formatter = percent_formatter
    for ss in series:
        gauge.add('Series 1', [{'value': ss.series1, 'max_value': 100}])
        gauge.add('Series 2', [{'value': ss.series2, 'max_value': 100}])

    some_name2 = gauge.render_data_uri()
    return some_name2