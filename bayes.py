import pickle

class Bayes(object):
	def __init__(self):
		self.pfc_map = {} 			# for PFC
		self.class_frequency = {}	# for PC
		self.feature_frequency = {} # for PF
		self.sample_size = 0.0		# for PFC, PC & PF

	# Offer data as a list of dicts [{'feature': "", 'class': ""}, ..]
	def train(self, data, append=False):
		if append:
			self.sample_size += len(data)
		else:
			self.sample_size = len(data)

		for record in data:
			self._update_pfc(record)
			self._update_pc(record)
			self._update_pf(record)

	# Both feature and klass are parameters of type String
	def classify(self, feature, klass):
		try:
			pfc = self._pfc(feature, klass)
			pc = self._pc(klass)
			pf = self._pf(feature)

			return  pfc * pc / pf
		except ZeroDivisionError:
			return 0.0

	# Saves a serialized version of the classifier
	def serialize(self, file):
		return pickle.dump(self, open(file, "wb"))

	# Loads a (pre-trained) serialized classifier
	@staticmethod
	def load(file):
		return pickle.load(open(file, "rb"))

	### PRIVATE METHODS ###

	def _update_pfc(self, record):
		try:
			self.pfc_map[record['class']][record['feature']] += 1.0
		except KeyError:
			try:
				self.pfc_map[record['class']][record['feature']] = 1.0
			except KeyError:
				self.pfc_map[record['class']] = {'feature_count': 0.0, record['feature']: 1.0}
		self.pfc_map[record['class']]['feature_count'] += 1.0
	
	def _update_pc(self, record):
		try:
			self.class_frequency[record['class']] += 1.0
		except KeyError:
			self.class_frequency[record['class']] = 1.0

	def _update_pf(self, record):
		try:
			self.feature_frequency[record['feature']] += 1.0
		except KeyError:
			self.feature_frequency[record['feature']] = 1.0

	def _pfc(self, feature, klass):
		try:
			feature_count = self.pfc_map[klass]['feature_count']
			feature_frequency = self.pfc_map[klass][feature]
			
			return feature_frequency / feature_count
		except KeyError:
			return 0.0

	def _pc(self, klass):
		try:
			return self.class_frequency[klass] / self.sample_size
		except KeyError:
			return 0.0

	def _pf(self, feature):
		try:
			return self.feature_frequency[feature] / self.sample_size
		except KeyError:
			return 0.0