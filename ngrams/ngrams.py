from bayes import Bayes
import openpyxl


class Ngrams(object):
    def __init__(self, ngrams_file):
        self.model = self.prepare_model(ngrams_file)

    # Load xlsx N-gram data
    def load_data(self, ngrams_file):
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

    # Prepare Bayes classifier
    def prepare_model(self, ngrams_file):
        try:
            return Bayes.load('bayes_classifier.p')
        except IOError:
            model = Bayes()
            model.train(self.load_data(ngrams_file))
            model.serialize('bayes_classifier.p')
            return model

    def classify(self, klass, feature):
        print Bayes.classify(self.model, klass, feature)
