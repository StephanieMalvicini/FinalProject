MAXIMUM_FAILING_PERCENTAGE = 0.1


class ListResult:

    def __init__(self, satisfies, list_name, list_result):
        self.satisfies = satisfies
        self.list_name = list_name
        self.list = list_result


class DoubleListResult(ListResult):

    def __init__(self, satisfies, first_list_name, first_list_result, second_list_name, second_list_result):
        ListResult.__init__(self, satisfies, first_list_name, first_list_result)
        self.second_list_name = second_list_name
        self.second_list = second_list_result


class TableResult:

    def __init__(self, satisfies, table_name, table):
        self.satisfies = satisfies
        self.table_name = table_name
        self.table = table


class PercentageWithDataFrameResult:

    def __init__(self, percentage, dataframe_name, dataframe):
        self.satisfies = percentage <= MAXIMUM_FAILING_PERCENTAGE
        self.percentage = percentage
        self.dataframe_name = dataframe_name
        self.dataframe = dataframe


class PercentageWithListResult:

    def __init__(self, percentage, list_name, list_result):
        self.satisfies = percentage <= MAXIMUM_FAILING_PERCENTAGE
        self.percentage = percentage
        self.list_name = list_name
        self.list_result = list_result


class ListOfResults:

    def __init__(self, all_satisfy, results):
        self.satisfies = all_satisfy
        self.list = results
