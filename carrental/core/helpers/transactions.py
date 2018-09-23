from datetime import timedelta
from graphos.sources.simple import SimpleDataSource
from graphos.renderers import gchart
from ..models import Transaction


def create_daterange(start_date, end_date):
    """
    Provides an array of dates between the provided start and end (inclusive).
    """
    date_range = []
    for i in range(int ((end_date - start_date).days)):
        date_range.append(start_date + timedelta(i))
    return date_range


def sort_by_day(transactions, date_range):
    """
    Creates a formatted list containing a set of headings and several sets of data.
    """
    ordered_data = {}
    for transaction in transactions:
        date_data = ordered_data.get(transaction.time.date(), [])
        date_data.append(transaction)
        ordered_data[transaction.time.date()] = date_data
    formatted_data = [
        ['Date', 'Pickups', 'Returns']
    ]
    for date in date_range:
        pickups = 0
        returns = 0
        date_transactions = ordered_data.get(date, [])
        for transaction in date_transactions:
            if transaction.type == 'PIC':
                pickups += 1
            else:
                returns += 1
        formatted_data.append([date.strftime('%d/%m'), pickups, returns])
    return formatted_data;       


def create_chart(transactions, start_date, end_date, chart_type):
    """
    Generates a chart of the chosen type using data provided.
    """
    if (chart_type == 'line'):
        date_range = create_daterange(start_date, end_date)
        ordered_data = sort_by_day(transactions, date_range)
        data_source = SimpleDataSource(ordered_data)
        return gchart.LineChart(data_source)


def get_transactions_by_dates(start_date, end_date):
    """
    Returns a list of transactions between the provided dates (inclusive).
    """
    return Transaction.objects.filter(
        time__gte=start_date
    ).filter(
        time__lte=end_date
    ).order_by('-time')
