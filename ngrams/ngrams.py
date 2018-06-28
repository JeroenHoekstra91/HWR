from bayes import Bayes
import openpyxl


class Ngrams(object):
    def __init__(self, model_path):
        self.load_model(model_path)

    # Prepare Bayes classifier
    def load_model(self, model_path):
        self.model = Bayes.load(model_path)

    def classify(self, klass, feature):
        return self.model.classify(klass, feature)

    @staticmethod
    def train_model(ngrams_file, output_file):
        model = Bayes()
        model.train(Ngrams._load_data(ngrams_file))
        model.serialize(output_file)

    #### PRIVATE METHODS ####

    # Load xlsx N-gram data
    @staticmethod
    def _load_data(ngrams_file):
        data = []
        workbook = openpyxl.load_workbook(ngrams_file)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, min_col=2):
            names = row[0].value
            frequencies = row[1].value

            klass = names.split('_')[-1]
            feature = '_'.join(names.split('_')[0:-1])

            # Expand data for use with the Bayesian classifier
            for i in range(int(frequencies)):
                data.append({
                        'class': klass,
                        'feature': feature
                    })
        return data