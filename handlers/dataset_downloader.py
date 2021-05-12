class DatasetDownloader:

    def __init__(self, dataset):
        self.dataset = dataset

    def download_dataset(self, path):
        self.dataset.to_csv(path, index=True, header=True)
