from matplotlib import pyplot as plt
from IPython.display import display


def get_graphs(for_churn, segment: str = None, state: str = None, city: str = None):

    if (segment is None) & (state is None) & (city is None):
        filtered_churn = for_churn.groupby('report_dt').sum().reset_index()
        text = 'Total'
    else:
        segment_filter = (lambda x: '' if x is None else f"segment == '" + x + "'")(segment)
        state_filter = (lambda x: '' if x is None else f"state == '" + x + "'")(state)
        city_filter = (lambda x: '' if x is None else f"city == '" + x + "'")(city)

        text = ' ,'.join([x for x in [city, state, segment] if x is not None])
        r = ' & '.join([x for x in [city_filter, state_filter, segment_filter] if len(x) > 0])
        filtered_churn = for_churn.query(r).groupby('report_dt').sum().reset_index()

    filtered_churn['active_shift'] = filtered_churn['active'].shift(1)
    filtered_churn['active_avg'] = (filtered_churn['active'] + filtered_churn['active_shift']) / 2
    filtered_churn['churn_rate'] = filtered_churn['become churn'] / filtered_churn['active_avg']
    filtered_churn['reactivation_rate'] = filtered_churn['reactivated'] / filtered_churn['active_avg']
    filtered_churn['avg_order'] = filtered_churn['sales'] / filtered_churn['orders_cnt']

    filtered_churn['year'] = filtered_churn['report_dt'].dt.year.astype('int')
    filtered_churn['churn'] = [1 - i for i in filtered_churn['churn_rate']]
    filtered_churn['reactivation'] = [1 - i for i in filtered_churn['reactivation_rate']]

    print('-------------ГОДОВАЯ ДИНАМИКА-------------')
    print('\n')
    test_1 = filtered_churn.groupby('year').prod()['churn'].reset_index()
    test_1['churn'] = (round(100 - test_1['churn'] * 100, 1)).astype('str') + '%'
    test_1 = test_1.T
    test_1.columns = test_1.iloc[0].astype('int')
    test_1 = test_1[1:]
    display(test_1)

    test_1 = filtered_churn.groupby('year').prod()['reactivation'].reset_index()
    test_1['reactivation'] = round(100 - test_1['reactivation'] * 100, 1).astype('str') + '%'
    test_1 = test_1.T
    test_1.columns = test_1.iloc[0].astype('int')
    test_1 = test_1[1:]
    display(test_1)

    test_1 = filtered_churn.groupby('year').sum()['sales'].reset_index()
    test_1['sales'] = test_1['sales'].astype('int')
    test_1 = test_1.T
    test_1.columns = test_1.iloc[0].astype('int')
    test_1 = test_1[1:]
    display(test_1)

    test_1 = filtered_churn.groupby('year').sum()['orders_cnt'].reset_index()
    test_1['orders_cnt'] = test_1['orders_cnt'].astype('int')
    test_1 = test_1.T
    test_1.columns = test_1.iloc[0].astype('int')
    test_1 = test_1[1:]
    display(test_1)

    test_1 = filtered_churn.groupby('year').mean()['avg_order'].reset_index()
    test_1['avg_order'] = round(test_1['avg_order'], 1)
    test_1 = test_1.T
    test_1.columns = test_1.iloc[0].astype('int')
    test_1 = test_1[1:]
    display(test_1)

    test_1 = filtered_churn.groupby('year').sum()['new'].reset_index()
    test_1['new'] = test_1['new'].astype('int')
    test_1 = test_1.T
    test_1.columns = test_1.iloc[0].astype('int')
    test_1 = test_1[1:]
    display(test_1)

    print('\n')
    print('-------------МЕСЯЧНАЯ ДИНАМИКА-------------')
    print('\n')
    fig, ax = plt.subplots(3, 2, figsize=(40, 20))

    ax[0, 0].plot(filtered_churn[['report_dt', 'churn_rate']].sort_values(by=['report_dt']).set_index('report_dt'))
    ax[0, 0].set_title(f'Churn Rate, % for {text}')

    dates = filtered_churn['report_dt']
    data_test = filtered_churn['churn_rate']

    for x, y in zip(dates, data_test):
        if y == 0:
            pass
        else:
            label = f'{round(y * 100, 1)}'
            ax[0, 0].annotate(label,
                              (x, y),
                              textcoords="offset points",
                              xytext=(-1, -10),
                              ha='center')

    ax[0, 1].plot(filtered_churn[['report_dt', 'reactivation_rate']].set_index('report_dt'))
    ax[0, 1].set_title(f'Reactivation Rate, % for {text}')

    dates = filtered_churn['report_dt']
    data_test = filtered_churn['reactivation_rate']

    for x, y in zip(dates, data_test):
        if y == 0:
            pass
        else:
            label = f'{round(y * 100, 1)}'
            ax[0, 1].annotate(label,
                              (x, y),
                              textcoords="offset points",
                              xytext=(-1, -10),
                              ha='center')

    ax[1, 0].plot(filtered_churn[['report_dt', 'sales']].set_index('report_dt'))
    ax[1, 0].set_title(f"Sales Volume'000 for {text}")

    dates = filtered_churn['report_dt']
    data_test = filtered_churn['sales']

    for x, y in zip(dates, data_test):
        if y == 0:
            pass
        else:
            label = int(y / 1000)
            ax[1, 0].annotate(label,
                              (x, y),
                              textcoords="offset points",
                              xytext=(-1, -10),
                              ha='center')

    ax[1, 1].plot(filtered_churn[['report_dt', 'orders_cnt']].set_index('report_dt'))
    ax[1, 1].set_title(f'Orders Count for {text}')

    dates = filtered_churn['report_dt']
    data_test = filtered_churn['orders_cnt']

    for x, y in zip(dates, data_test):
        if y == 0:
            pass
        else:
            label = int(y)
            ax[1, 1].annotate(label,
                              (x, y),
                              textcoords="offset points",
                              xytext=(-1, -10),
                              ha='center')

    ax[2, 0].plot(filtered_churn[['report_dt', 'avg_order']].set_index('report_dt'))
    ax[2, 0].set_title(f'Average Order for {text}')

    dates = filtered_churn['report_dt']
    data_test = filtered_churn['avg_order']

    for x, y in zip(dates, data_test):
        if y == 0:
            pass
        else:
            label = int(y)
            ax[2, 0].annotate(label,
                              (x, y),
                              textcoords="offset points",
                              xytext=(-1, -10),
                              ha='center')

    ax[2, 1].plot(filtered_churn[['report_dt', 'new']].set_index('report_dt'))
    ax[2, 1].set_title(f'New clients for {text}')

    dates = filtered_churn['report_dt']
    data_test = filtered_churn['new']

    for x, y in zip(dates, data_test):
        if y == 0:
            pass
        else:
            label = int(y)
            ax[2, 1].annotate(label,
                              (x, y),
                              textcoords="offset points",
                              xytext=(-1, -10),
                              ha='center')
    plt.show()